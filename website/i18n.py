"""
Website languages, following the expoBridge approach.

English is the source language of every page. For another language, the finished HTML
is translated on the server from website/locale/<code>.json (English text -> translation),
so search engines index each language version. Text without a translation stays English.
Elements marked translate="no", scripts and styles are never touched.

Language choice: ?lang=xx (remembered in a cookie for a year) -> cookie -> browser language -> English.
"""
import html as htmlmod
import json
import re
from functools import lru_cache
from pathlib import Path

DEFAULT = "en"
COOKIE = "tg_lang"
LANGS = {
    "en": {"name": "English", "flag": "gb", "og": "en_GB"},
    "de": {"name": "Deutsch", "flag": "de", "og": "de_DE"},
    "fr": {"name": "Français", "flag": "fr", "og": "fr_FR"},
    "pt": {"name": "Português", "flag": "pt", "og": "pt_PT"},
    "es": {"name": "Español", "flag": "es", "og": "es_ES"},
}
LOCALE_DIR = Path(__file__).resolve().parent / "locale"
ATTRS = ("placeholder", "aria-label", "title", "alt")
META_KEYS = {"description", "twitter:title", "twitter:description", "og:title", "og:description", "og:image:alt"}
RAW = ("script", "style", "textarea", "code", "pre", "noscript")
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
MONTHS_EN = ["January", "February", "March", "April", "May", "June", "July", "August",
             "September", "October", "November", "December"]
DATE_RE = re.compile(r"^[\d–\- ]*(?:%s)(?: \d{4})?(?: – [\d ]+(?:%s) \d{4})?$" % ("|".join(MONTHS_EN), "|".join(MONTHS_EN)))
MONTH_RE = re.compile(r"\b(%s)\b" % "|".join(MONTHS_EN))
TAG_RE = re.compile(r"<(/?)([a-zA-Z][a-zA-Z0-9:-]*)([^>]*)>", re.S)
ATTR_RE = re.compile(r'(\s)([a-zA-Z:-]+)="([^"]*)"')


def choose(request):
    asked = (request.GET.get("lang") or "").lower()
    if asked in LANGS:
        return asked, True
    saved = request.COOKIES.get(COOKIE, "")
    if saved in LANGS:
        return saved, False
    for part in (request.META.get("HTTP_ACCEPT_LANGUAGE") or "").split(","):
        code = part.split(";")[0].strip().lower()[:2]
        if code in LANGS:
            return code, False
    return DEFAULT, False


@lru_cache(maxsize=8)
def load(code):
    path = LOCALE_DIR / f"{code}.json"
    if code == DEFAULT or not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


class Translator:
    def __init__(self, code):
        self.code = code
        data = load(code)
        self.dict = {k: v for k, v in data.items() if not k.startswith("__")}
        self.months = data.get("__months") or MONTHS_EN
        self.patterns = [(re.compile(p), r) for p, r in data.get("__patterns", [])]

    def lookup(self, text):
        key = " ".join(text.split())
        if not key or len(key) > 1200:
            return None
        if key in self.dict:
            return self.dict[key]
        if DATE_RE.match(key):
            return MONTH_RE.sub(lambda m: self.months[MONTHS_EN.index(m.group(1))], key)
        for rx, rep in self.patterns:
            if rx.match(key):
                return rx.sub(rep, key)
        if key.endswith("…") and len(key) > 20:
            stem = key[:-1].rstrip()
            for k, v in self.dict.items():
                if k.startswith(stem):
                    return v[: len(stem)].rstrip() + "…"
        return None

    def text(self, raw):
        plain = htmlmod.unescape(raw)
        found = self.lookup(plain)
        if found is None:
            return raw
        lead = raw[: len(raw) - len(raw.lstrip())]
        trail = raw[len(raw.rstrip()):]
        return lead + htmlmod.escape(found, quote=False) + trail

    def tag(self, tag_html, name, attrs_str):
        attrs = dict((k.lower(), v) for _, k, v in ATTR_RE.findall(attrs_str))
        targets = set(ATTRS)
        if name == "meta" and (attrs.get("name") in META_KEYS or attrs.get("property") in META_KEYS):
            targets.add("content")
        if name == "input" and attrs.get("type") in ("submit", "button"):
            targets.add("value")

        def sub(m):
            if m.group(2).lower() not in targets:
                return m.group(0)
            found = self.lookup(htmlmod.unescape(m.group(3)))
            if found is None:
                return m.group(0)
            return f'{m.group(1)}{m.group(2)}="{htmlmod.escape(found, quote=True)}"'

        return ATTR_RE.sub(sub, tag_html)

    def html(self, page):
        if not self.dict:
            return page
        out, pos, stack = [], 0, []  # stack: [tag, blocked]
        n = len(page)
        while pos < n:
            lt = page.find("<", pos)
            if lt == -1:
                lt = n
            if lt > pos:
                chunk = page[pos:lt]
                out.append(chunk if (stack and stack[-1][1]) or not chunk.strip() else self.text(chunk))
                pos = lt
                continue
            if page.startswith("<!--", pos):
                end = page.find("-->", pos)
                end = n if end == -1 else end + 3
                out.append(page[pos:end]); pos = end
                continue
            m = TAG_RE.match(page, pos)
            if not m:
                out.append("<"); pos += 1
                continue
            closing, name, attrs = m.group(1) == "/", m.group(2).lower(), m.group(3)
            blocked = bool(stack and stack[-1][1])
            if closing:
                for i in range(len(stack) - 1, -1, -1):
                    if stack[i][0] == name:
                        del stack[i:]
                        break
                out.append(m.group(0)); pos = m.end()
                continue
            out.append(m.group(0) if blocked else self.tag(m.group(0), name, attrs))
            pos = m.end()
            if name in RAW:
                end = page.lower().find(f"</{name}", pos)
                end = n if end == -1 else end
                out.append(page[pos:end]); pos = end
                continue
            if name not in VOID and not attrs.rstrip().endswith("/"):
                stack.append([name, blocked or 'translate="no"' in attrs])
        return "".join(out)


def translate_page(page, code):
    if code == DEFAULT:
        return page
    return Translator(code).html(page)
