# TradeGate Website — Progress Tracker

Last updated: 2026-11-14 · Owner: Ivan Nkomati

Update after every meaningful change. Record evidence; do not turn plans into completion claims.

## Current state

Live on `main` (last deploy 2026-11-14 05:50, commit 62d99d8 + this context pack). All 47 tests pass. Branch `feature/service-packages` mirrors `main`.

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
| 2026-11-14 | Six context files + entry files | this commit |

## Known issues / open questions

| ID | Issue | Status |
| --- | --- | --- |
| EVT-001 | Owner reported "event calendars removed" after the language release. Code check: German calendar (home marquee + /trade-fairs/) renders in EN and DE. Partner events section is empty live because both events are unpublished (they were shown in the preview only). | Waiting for owner: publish partner events? / screenshot of what is missing |
| SEO-001 | Google still shows grey globe until it recrawls; owner to request indexing in Search Console | Waiting for Google |
| SEO-002 | Search Console / Bing verification codes not yet set (`GOOGLE_SITE_VERIFICATION`, `BING_SITE_VERIFICATION`) | Owner |
| MEDIA-001 | Confirm nginx serves `/media/` (needed for partner logos/banners once published) | Unverified |
| FAIR-001 | MEDICA 2027 dates unconfirmed (Team France lists 15–18 Nov 2027) | Watch organiser |
| I18N-001 | Text added later in admin (new fairs, prices) stays English in other languages until added to `website/locale/*.json` | By design; translate on request |

## Next steps (owner's order)

1. Resolve EVT-001.
2. When Aviana is countersigned: tick materials permission + published; upload official logo/banner/brochure (no organiser contacts on them).
3. Search Console + Google Business Profile.
4. Optional: FAQ editable in admin.
