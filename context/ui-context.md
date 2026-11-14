# TradeGate Website — UI Context

## Brand

- Colours: navy `#07111F` (ink/primary), gold `#D6B36A` (accent), copper `#A56A43`, ivory `#F7F2EA` (page background), muted `#8CA3B8`. Brand colours come from Site settings via CSS variables (`--tg-primary/accent/muted`).
- Fonts: Sora (headings, `font-display`), DM Sans (body).
- Logo: gateway "TG" logo, `static/website/img/tradegate-logo-light.webp` (header h-11/md:h-14, footer). Icons: `favicon.ico`, `favicon-48/96/192/512.png`, `apple-touch-icon.png`.
- Social preview: `static/og-default.png` (1200×630, current logo); old version kept as `og-default-2025.png`.

## Approved, protected UI (do not remove or redesign without the owner asking)

1. Header: logo, Home, Services dropdown (incl. "For trade-fair organisers"), Trade fair calendar, FAQs, About, **language picker (flags)**, gold "Request consultation" button; mobile: flag picker + menu button.
2. Home: dark hero with "Your market-entry team on the ground in Germany."; service cards with summary, from-price, "Full description" and "Packages" links; dark **"Our partner trade fairs"** section; **German trade-fair marquee** ("Going to a trade fair in Germany? Let us work it for you."), pauses on hover, respects reduced motion.
3. Trade fair calendar page: partner events (cards with banner/placeholder), German fairs by month with **category filter chips**, organiser CTA, disclaimer.
4. Fair detail: hero with "At a glance" box; partner banner or branded placeholder with event logo and "Official event banner coming soon" badge; package list with prices right-aligned; .ics link.
5. Service pages: "At a glance", packages, commission terms, "What we need from you", "What is not included", FAQ.
6. About: founder card (view-only photo, LinkedIn), partners text, "Partner with us" section.
7. Contact: enquiry form with optional fields folded in `<details>`.
8. Footer: logo, services, company links incl. Partner events and Partner with us, LinkedIn, legal links.
9. Admin: navy/gold theme, grouped sections (Enquiries, Trade fairs, Services and prices, Team and company, Website structure, Users and access), dashboard stats.

## Rules

- Change only what is asked. A feature request is never a reason to drop, hide or restyle another section.
- Before pushing, compare screenshots of home, trade-fairs, a fair page, a service page, about and contact (desktop 1280 and phone 390) with the previous version.
- A section that depends on admin data (partner events) must be explained to the owner if it is empty on the live site.
