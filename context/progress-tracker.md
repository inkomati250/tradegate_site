# TradeGate Website — Progress Tracker

Last updated: 2026-11-15 · Owner: Ivan Nkomati

Update after every meaningful change. Record evidence; do not turn plans into completion claims.

## Current state

Live on `main` (deploy 2026-11-14 08:06, commit 61fda3f). Live PostgreSQL now at migration 0022. All tests pass. Branch `feature/service-packages` mirrors `main`.

## Live 2026-11-15 (from branch `feature/partner-hub`)

- **HUB-001 TradeGate Partner Hub, phase 1** (2026-11-15): `/partner-hub/` registration page (5 languages), PartnerProfile model (0024), admin review + suggested matches + dashboard card, owner email per registration, menu/footer links, CTA on partner-search and distributor-search pages, sitemap entry, privacy policy section 10 DE+EN + language-cookie note (0025). Desktop nav made to fit one line at 1024px (language name shown from 1280px). Evidence: 57 tests pass; screenshots desktop/mobile/DE/admin checked. Round 2 (owner feedback): worldwide wording (no Africa/Middle East/Asia examples: footer badge, FAQ, About chips, market-entry meta), Partner Hub vs "Partner with us" cross-links, lighter hub link on service pages. Preview artifact: https://claude.ai/artifact/SvGfRyXhbjwiLg8cigSDJ1. Round 3: admin redesign (top menu instead of left sidebar, new dashboard: KPIs, open enquiries, newest hub companies with match counts, fairs in next 4 months), hub admin with tick-boxes and status badges, optional confirmation email to registering companies in their language (Site Settings → Partner Hub, OFF by default until owner approves the text, 0026). Owner approved push 2026-11-15. 60 tests pass.

- **FIX-CACHE-001** (2026-11-15): after the Partner Hub deploy the owner saw an unstyled admin and cramped menu. Cause: nginx serves /static/ with 30-day browser caching and the CSS URLs never changed, so browsers kept the old CSS. Fix: CSS links carry `?v=<hash of the CSS files>` (context processor `asset_v`), so every CSS change reaches visitors immediately. Partner Hub icons also have fixed width/height.
- **STATS-001 Visitor statistics** (2026-11-15): cookieless first-party statistics (`analytics.py`, `PageVisit`, `VisitStatsMiddleware`): daily unique visitors, page views, countries (DB-IP Country Lite, downloaded monthly by `deploy_manage.sh` to /srv/tradegate/geo/), sources (Google, LinkedIn, AI assistants…), pages, devices, languages, visit-to-lead rates. No IP stored, daily-rotating visitor hash, staff/bots/DNT/GPC not counted, 13-month retention (`prune_visits` on every deploy). Admin: "Visitors" menu + dashboard panels. Privacy policy section 11 DE+EN (migration 0028).

- **UI-HDR-001** (2026-11-15, owner request): header background made fully solid navy (#07111F). It was 95% opaque since June, so at the top of the page the cream page background showed through and the logo looked duller than when scrolled. Logo file and size unchanged (verified pixel-identical).

- **STATS-002** (2026-11-15): first hours of statistics were inflated by scanners (103 "visitors", 1 view each, 27 countries, all direct). Counting now happens only when a real browser runs a tiny script and reports the view to `/v/` (headless/automation, bot user agents, DNT/GPC, staff excluded); one person = one visitor per day. Old rows reset (0029). Inquiry list: Save button readable, company column.

- **WA-001** (2026-11-15, owner request): footer WhatsApp opens a window with a QR code (scan with the phone; WhatsApp opens with a ready greeting) instead of an external link; on phones it opens WhatsApp directly. QR made with segno from Site Settings → WhatsApp URL; verified the rendered code decodes to the right link.
- **SPAM-002** (2026-11-15): both forms: signed start time (bots can no longer fake an old form), keyboard-mash detection (German compounds safe), more spam keywords, rate limit now shared by all gunicorn workers (file cache in prod). Existing honeypot, CSRF, timing and link checks kept.

- **SOC-001** (2026-11-15): footer "Get in touch" now shows Facebook, Instagram and X when filled in under Site Settings (only LinkedIn was ever shown; the other fields were stored but not displayed). Direct links, no QR window (decided: QR only for WhatsApp, where the chat lives on the phone).

## Completed (all live)

| Date | Change | Evidence |
| --- | --- | --- |
| 2026-11-13/14 | Service packages, detailed service cards, organiser page, founder section, LinkedIn, view-only founder photo (v3), new gateway logo and favicons | Commits 37b2ae4 … 90693ca; owner reviewed in preview |
| 2026-11-14 | Trade fair calendar (39 German fairs 2027, by month, sector filter), homepage marquee, fair detail pages, .ics, Event schema | a6e9d9e, f1f4e79 |
| 2026-11-14 | Partner events separated; admin-editable packages, team and fairs; branded admin | 5fa5d41 |
| 2026-11-14 | Two partner events (Aviana, Azerbaijan) with descriptions, organiser prices, logos, "banner coming soon" placeholder, price-list image field | 1a257c3 |
| 2026-11-14 | Partner events never show organiser link/name; German fairs show "Official link not available" when no link; Asia-Pacific Sourcing URL fixed | ee2dcea, 3a9e81d |
| 2026-11-14 | SEO: compiled CSS (faster), full meta/OG/Twitter tags, business/service/FAQ/breadcrumb/event schema, complete sitemap, new social image | fd0577b |
| 2026-11-14 | Five languages (EN/DE/FR/PT/ES) with flag picker; favicon fix for Google results | 62d99d8; coverage script showed only identical words/company names untranslated |
| 2026-11-14 | Six context files + entry files | c388056 |
| 2026-11-14 | Deploy now migrates the LIVE database (with backup first); partner events published as in the approved preview | this commit |

## Known issues / open questions

| ID | Issue | Status |
| --- | --- | --- |
| EVT-001 | Live calendar empty and partner section missing. Root cause (read-only server diagnostics 2026-11-14): the deploy ran `migrate` without the live settings, so it migrated a local SQLite file; live PostgreSQL `tradegate_db` stayed at migration 0008 (0009–0021 never applied, no TradeFair/ServicePackage/TeamProfile tables). Fix: `scripts/deploy_manage.sh` loads `/srv/tradegate/.env`, backs up the live DB to `/srv/tradegate/backups/` before migrating, then migrates the live DB. Owner asked to show the two partner events as in the preview (migration 0022). | Fixed and verified 2026-11-14 08:07: live home shows partner section (both logos) + German carousel; /trade-fairs/ lists all fairs; DE/FR versions; logos/CSS/favicon served (200); 0 organiser links/names; backup db-20261114-070630.dump |
| SEO-001 | Google still shows grey globe until it recrawls; owner to request indexing in Search Console | Waiting for Google |
| SEO-003 | Sitemap listed all 267 URLs under example.com (Django Sites default) → Search Console "URL not allowed". Fixed 15 Nov 2026: sitemaps use DJANGO_SITE_URL / Site domain / www.tradegateconsultants.com; migration 0023 sets the Site domain. Resubmitted: Success, 267 pages discovered | Done |
| SEO-002 | Search Console / Bing verification codes not yet set (`GOOGLE_SITE_VERIFICATION`, `BING_SITE_VERIFICATION`) | Owner |
| MEDIA-001 | nginx serves `/media/` | Verified 2026-11-14 (logos 200 image/webp) |
| FAIR-001 | MEDICA 2027 dates unconfirmed (Team France lists 15–18 Nov 2027) | Watch organiser |
| I18N-001 | Text added later in admin (new fairs, prices) stays English in other languages until added to `website/locale/*.json` | By design; translate on request |

## Next steps (owner's order)

1. Resolve EVT-001.
2. When Aviana is countersigned: tick materials permission + published; upload official logo/banner/brochure (no organiser contacts on them).
3. Search Console + Google Business Profile.
4. Optional: FAQ editable in admin.
