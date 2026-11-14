# TradeGate Website — Architecture

## Stack

- Django 5.0.2, Python 3; gunicorn behind nginx on the VPS; PostgreSQL in production (env-configured), SQLite locally (`db.sqlite3`, never committed).
- Settings: `tradegate/settings/{base,dev,prod}.py`, values from environment (`env`, `env_bool`).
- Styling: Tailwind compiled to `website/static/website/css/site.css` (config in `tailwind/`, rebuild with `bash scripts/build_css.sh`, commit the CSS). `DJANGO_USE_TAILWIND_CDN=true` switches back to the old CDN script without a code change.
- Fonts: Google Fonts (Sora, DM Sans). No JS framework; small inline scripts.

## Deployment

`.github/workflows/deploy-prod.yml` on push to `main`: fetch + `reset --hard origin/main`, pip install, `makemigrations --check`, `check --deploy`, `migrate`, `collectstatic`, restart gunicorn, reload nginx. Media: `/srv/tradegate/media` (outside the app folder). Static: `/srv/tradegate/staticfiles`.

**Pushing to `main` = going live.** Only with the owner's go-ahead.

Backups: branches `backup/pre-overhaul-2026-11-14` (site before the overhaul, 045e7a4) and `backup/pre-seo-2026-11-14` (3a9e81d). Tags cannot be pushed from the assistant environment; use backup branches. Every change is a separate commit, revertable on its own.

## App `website`

| Area | Files |
| --- | --- |
| Models | `models.py`: SiteSettings, NavigationItem, Inquiry, LegalPage, Service/Industry/ProcessStep, **TradeFair** (kind `germany`/`represented`, materials_permission, logo, cover_image, brochure, packages_text, packages_image, packages_note, is_published, show_in_carousel), **ServicePackage**, **TeamProfile** |
| Static content | `content.py`: SERVICE_PAGES, SERVICE_NAV, ORGANISER_NAV, FOUNDER, FAIR_DISCLAIMER, FAIR_CATEGORIES (DB packages/team override these when present) |
| Views | `views.py`: home, service_landing, trade_fairs, trade_fair_detail, trade_fair_ics, contact (saves Inquiry, emails CONTACT_RECIPIENT_EMAIL, spam/rate-limit checks), about, faq, legal_page |
| SEO | `seo.py` (Organization/ProfessionalService + WebSite schema on every page, breadcrumbs, FAQPage), `sitemaps.py` (static, services, legal, trade fairs, translated versions), robots.txt, `/favicon.ico`, `/site.webmanifest` in `tradegate/urls.py` |
| Languages | `i18n.py` + `middleware.py` (LanguageMiddleware) + `locale/{de,fr,pt,es}.json`; picker `templates/website/partials/lang_picker.html` |
| Admin | `admin.py` + `templates/admin/` + `static/website/admin/tradegate-admin.css` |
| Seeds | migrations 0013/0015/0016/0018 seed fairs, packages, founder, partner events; seed logos in `website/seed/` |

## Invariants

- Partner events (`kind=represented`): published only with `materials_permission`; `official_url` is cleared on save; organiser name and links never rendered.
- German fairs: link to the official site only if `official_url` is set, otherwise "Official link not available".
- Contact form: every valid enquiry is saved; email failure never loses the enquiry; emails stay English.
- Translations happen on finished HTML; scripts, styles, JSON-LD and `translate="no"` elements are never touched. Admin, static, media, sitemap are never translated.
- Founder photo is a CSS background (not downloadable by right-click).
- Migrations must not fail on a read-only media folder.
