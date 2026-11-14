# TradeGate Website — Code Standards

## Django

- Keep logic in views/models/helpers; templates stay presentational. Follow the existing style of `website/`.
- Every model change gets a migration; `python manage.py makemigrations --check` must be clean before pushing.
- Data migrations: idempotent (`get_or_create`, only touch what they own), never delete published or user-edited data, tolerate a read-only media folder.
- Anything the owner changes regularly (events, prices, packages, team, texts that change) must be editable in Django admin.
- No new dependencies without need; the server installs `requirements.txt` on deploy.

## Front end

- Tailwind classes in templates; after adding new classes run `bash scripts/build_css.sh` and commit `website/static/website/css/site.css`.
- Custom CSS that Tailwind cannot express goes in the `<style>` block of `base.html` (or the page template).
- Images: always `alt`; logos with width/height; lazy-load below the fold.
- Accessibility: keyboard reachable menus, visible focus, `prefers-reduced-motion` respected.

## Languages

- English is the source text. New visible text → add translations to `website/locale/{de,fr,pt,es}.json` (key = exact English text, whitespace-normalised).
- Text that must not be translated: wrap in an element with `translate="no"`.

## Checks before every push

1. `DJANGO_SETTINGS_MODULE=tradegate.settings.dev python manage.py test website` (currently 47 tests, all must pass).
2. `makemigrations --check --dry-run` clean.
3. `check --deploy` with prod settings (warnings W004 HSTS and dummy-key W009 are known).
4. Visual check of the protected pages (see ui-context.md).
5. Commit as "Ivan Nkomati <inkomati@tradegateconsultants.com>" with the session attribution lines.
