from django.utils.cache import patch_vary_headers

from . import i18n

SKIP_PREFIXES = ("/admin", "/static", "/media", "/sitemap.xml", "/robots.txt", "/favicon.ico", "/health")


class LanguageMiddleware:
    """Picks the visitor's language and translates finished website pages (see website/i18n.py)."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        code, explicit = i18n.choose(request)
        request.LANGUAGE_CODE = code
        response = self.get_response(request)
        if request.path.startswith(SKIP_PREFIXES):
            return response
        if explicit:
            response.set_cookie(i18n.COOKIE, code, max_age=60 * 60 * 24 * 365, samesite="Lax")
        content_type = response.get("Content-Type", "")
        if (code != i18n.DEFAULT and "text/html" in content_type and not getattr(response, "streaming", False)
                and response.status_code == 200):
            charset = response.charset or "utf-8"
            page = response.content.decode(charset)
            response.content = i18n.translate_page(page, code).encode(charset)
            if response.has_header("Content-Length"):
                response["Content-Length"] = str(len(response.content))
        response["Content-Language"] = code
        patch_vary_headers(response, ("Cookie", "Accept-Language"))
        return response


class VisitStatsMiddleware:
    """Counts page views for the admin statistics (cookieless; see analytics.py)."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        from . import analytics
        analytics.record(request, response)
        return response
