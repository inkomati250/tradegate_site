# TradeGate Consultants Website — Project Overview

Last updated: 2026-11-14 · Owner: Ivan Nkomati · Live: tradegateconsultants.com

## What this is

The public website of **TradeGate Consultants**, a Leipzig-based sole proprietorship (Ivan Nkomati, trading as TradeGate Consultants) that helps international companies enter Germany and the EU. Django 5.0.2, deployed automatically on every push to `main` (GitHub Actions, self-hosted runner on the VPS).

Separate from expoBridge (the Laravel SaaS). Do not mix code, wording or context between the two.

## Business model (what the site must sell)

Main services, each with its own page, packages and "from" prices (editable in admin):

| Service | Page slug | Pricing model |
| --- | --- | --- |
| Trade fair representation in Germany | `trade-fair-representation-germany` | From €650 per fair day |
| Find business partners in Germany | `find-business-partners-germany` | From €490 + €1,200 success fee per signed partner |
| Distributor search in Germany | `distributor-search-germany` | From €490 + €1,200 per signed distributor |
| Germany market-entry support | `germany-market-entry-support` | From €390 |
| Local EU representative presence | `eu-local-representative-germany` | From €290/month |
| Trade fair follow-up and lead management | `trade-fair-follow-up-lead-management` | From €350 |
| Exhibitor recruitment (for organisers) | `exhibitor-recruitment-germany` | Commission only, non-exclusive |

Owner decisions that stand:

- Exhibitor recruitment is an **added** service for trade-fair organisers, not the main service.
- "Foot in the door" entry packages with "from" prices that leave room to negotiate.
- Copy says **"we"**, never "I". It may hint at a partner network but never names partners. Consultants and agents are invited to join ("Partner with us").
- Recruitment is **non-exclusive**, for exhibitors from Germany, the EU and beyond.
- Ivan is shown as founder (photo view-only, LinkedIn links).

## Audiences

1. International SMEs/exporters (Africa, Middle East, Asia especially) wanting Germany/EU access without an office.
2. Trade-fair organisers abroad who want exhibitors/sponsors from Germany and the EU.
3. Independent consultants and agents who want to cooperate.

## Pages and features (all must keep working)

- Home: hero, service cards with description and package links, **partner trade fairs section** (shows only published partner events), **German trade-fair carousel** (right-to-left marquee), process, CTA.
- **Trade fair calendar** `/trade-fairs/`: partner events block + 39 German fairs grouped by month, sector filter chips, organiser CTA, disclaimer.
- Fair detail pages `/trade-fairs/<slug>/`: banner (official or "coming soon" placeholder), packages/prices, who should exhibit/visit, how we help, .ics download, Event schema.
- Seven service pages, About (founder card, partners), FAQ, Contact (enquiry form → database + email), legal pages (Impressum, Datenschutz).
- **TradeGate Partner Hub** `/partner-hub/` (menu link "Partner Hub"): private B2B company network. Companies (any country → Germany/EU, and German/EU → abroad) register a profile; we approve, the system suggests matches in admin, we introduce personally. Never public, never automatic contact. Phase 1 (registration + admin matching) built 2026-11-15; later phases: company logins/profiles, anonymous public opportunity board with "I'm interested" routed through us.
- **Five languages** (EN/DE/FR/PT/ES) with flag picker in the nav. Owner decided 2026-11-15: no further languages for now.
- Branded Django admin (navy/gold, grouped sections, dashboard stats).

## Partner events (current state)

| Event | Agreement | Website status |
| --- | --- | --- |
| ECOWAS Aviana West Africa International Expo 2027 (Ibadan, 22–24 June 2027) | Signed by organiser 13 Nov 2026; Ivan's review/countersignature pending | Published with description, USD prices, logo (migration 0022, owner request) |
| Azerbaijan Mining Expo 2027 (Baku, 8–10 Sept 2027) | Agreement in redlines | Published with description, EUR prices, logo (migration 0022, owner request) |

Partner events appear on the live site only when **both** "materials permission" and "published" are ticked in admin. Organiser websites, contact details and organiser company names are **never** shown for partner events (we are the middleman).

## Out of scope unless the owner asks

Online payments, customer accounts (until Partner Hub phase 2 is approved), blog, live chat, changing the expoBridge project.
