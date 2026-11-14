"""Static marketing content for SEO landing pages and homepage opportunity cards.

Kept outside settings/deployment code so the site can be upgraded safely without
changing environment-specific configuration.
"""

SERVICE_PAGES = {
    "trade-fair-representation-germany": {
        "slug": "trade-fair-representation-germany",
        "service_code": "trade_fair",
        "kicker": "Trade fair representation Germany",
        "title": "Trade Fair Representation in Germany for International SMEs",
        "subtitle": "Attend German and EU trade fairs without sending a full team. TradeGate represents your company, captures qualified leads, documents conversations, and manages follow-up from Leipzig.",
        "primary_keyword": "trade fair representation Germany",
        "meta_title": "Trade Fair Representation Germany | TradeGate Consultants",
        "meta_description": "Germany trade fair representation for international SMEs: booth support, visitor outreach, lead capture, event reporting and follow-up from Leipzig.",
        "hero_badges": ["Germany-based", "Lead capture", "Photos + report", "Follow-up support"],
        "pain_points": [
            "You want EU exposure but travel, hotels and staff costs are high.",
            "You need someone on the ground who understands German business expectations.",
            "You do not only want photos from an event — you want useful contacts and next steps.",
        ],
        "deliverables": [
            "Pre-event briefing and target visitor/profile definition",
            "Trade fair attendance or booth support under your agreed brief",
            "Lead list with notes, contact details where available, and qualification remarks",
            "Photos, short clips and practical event observations",
            "Post-event summary report and recommended follow-up actions",
        ],
        "process": [
            ("Brief", "We define your offer, target buyers, event objective and must-meet contacts."),
            ("Represent", "We attend or support the event professionally and collect structured information."),
            ("Report", "You receive practical deliverables, not vague impressions."),
            ("Follow up", "We help convert interest into calls, introductions or partner discussions."),
        ],
        "faq": [
            ("Can you represent us if we are not travelling to Germany?", "Yes. The service is designed for companies that need a credible local presence without sending a full delegation."),
            ("Do you sell directly on our behalf?", "We can support lead generation, introductions and follow-up. Commercial commitments are agreed case by case and documented clearly."),
            ("What kind of companies is this for?", "Export-ready SMEs, manufacturers, food and beverage producers, tourism bodies, technology firms and service companies preparing for the German or EU market."),
        ],
        "related": ["find-business-partners-germany", "trade-fair-follow-up-lead-management", "germany-market-entry-support"],
    },
    "find-business-partners-germany": {
        "slug": "find-business-partners-germany",
        "service_code": "scouting",
        "kicker": "Partner search Germany",
        "title": "Find Business Partners and Distributors in Germany",
        "subtitle": "TradeGate helps international SMEs identify, approach and qualify potential distributors, resellers, sourcing partners and strategic contacts in Germany and the EU.",
        "primary_keyword": "find business partners Germany",
        "meta_title": "Find Business Partners in Germany | TradeGate Consultants",
        "meta_description": "Partner and distributor search in Germany for international SMEs: target mapping, outreach support, qualification and follow-up.",
        "hero_badges": ["Distributor search", "B2B outreach", "Germany/EU", "Qualified shortlist"],
        "pain_points": [
            "You do not know which German companies are relevant for your product or service.",
            "Cold emails without local context often receive no reply.",
            "You need a structured shortlist, not hundreds of unqualified contacts.",
        ],
        "deliverables": [
            "Target partner profile and search criteria",
            "Shortlist of potential distributors, resellers, buyers or strategic partners",
            "Localized approach messaging and outreach support",
            "Qualification notes and prioritization",
            "Next-step recommendations for calls, samples, meetings or events",
        ],
        "process": [
            ("Define", "We clarify your ideal partner, market segment and value proposition."),
            ("Map", "We research and organize potential partners by relevance."),
            ("Approach", "We support outreach with a German/EU market-aware message."),
            ("Qualify", "We separate serious prospects from low-fit contacts."),
        ],
        "faq": [
            ("Can you guarantee distributors?", "No serious consultancy should guarantee a partner without market validation. We can create a structured path to identify and qualify real opportunities."),
            ("Do you contact companies directly?", "Yes, where agreed in the scope. We can support outreach, introduction handling and follow-up."),
            ("Is this only for Germany?", "Germany is the core entry point, but the same structure can support wider EU partner search."),
        ],
        "related": ["distributor-search-germany", "germany-market-entry-support", "eu-local-representative-germany"],
    },
    "germany-market-entry-support": {
        "slug": "germany-market-entry-support",
        "service_code": "scouting",
        "kicker": "Germany / EU market entry",
        "title": "Germany Market Entry Support for International SMEs",
        "subtitle": "A practical bridge into Germany and the EU: positioning, first contacts, trade fair planning, partner search, and local execution support.",
        "primary_keyword": "Germany market entry support",
        "meta_title": "Germany Market Entry Support | TradeGate Consultants",
        "meta_description": "Practical Germany and EU market entry support for SMEs from Africa, the Middle East and Asia: strategy, partner search, trade fairs and local presence.",
        "hero_badges": ["Market entry", "Germany + EU", "SME focused", "Lean execution"],
        "pain_points": [
            "You want to enter Europe but are not ready for a branch office.",
            "You need to understand which entry route is realistic first.",
            "You need action, not a long theoretical market report.",
        ],
        "deliverables": [
            "Market entry starting-point assessment",
            "Recommended route: trade fair, partner search, local representation or staged approach",
            "Localized positioning and practical sales material review",
            "First outreach and opportunity mapping",
            "Clear action plan with realistic next steps",
        ],
        "process": [
            ("Assess", "We review your readiness, offer and target buyers."),
            ("Position", "We shape the message for German/EU business expectations."),
            ("Activate", "We start with a lean, measurable entry activity."),
            ("Scale", "Successful signals become deeper partner and follow-up work."),
        ],
        "faq": [
            ("Do we need an office in Germany first?", "Not necessarily. Many companies can begin with representation, trade fair validation or partner search before committing to a physical office."),
            ("Which regions do you support?", "TradeGate is especially positioned for SMEs from Africa, the Middle East and Asia seeking access to Germany and the EU."),
            ("Can you help with sales?", "We support the path to sales through positioning, partner discovery, qualified leads and follow-up. Sales responsibility and commercial authority are agreed clearly."),
        ],
        "related": ["eu-local-representative-germany", "find-business-partners-germany", "trade-fair-representation-germany"],
    },
    "eu-local-representative-germany": {
        "slug": "eu-local-representative-germany",
        "service_code": "local_presence",
        "kicker": "Local EU presence",
        "title": "Local EU Representative Presence from Germany",
        "subtitle": "Create a credible contact point in Germany without opening an office. TradeGate can support meetings, follow-up, event presence and relationship management from Leipzig.",
        "primary_keyword": "EU local representative Germany",
        "meta_title": "EU Local Representative Germany | TradeGate Consultants",
        "meta_description": "Local EU representative presence for international SMEs: Germany-based contact support, trade fairs, meetings, follow-up and partner coordination.",
        "hero_badges": ["Leipzig-based", "Local contact", "No branch office", "B2B trust"],
        "pain_points": [
            "Prospects prefer a local European contact point.",
            "You are not ready to hire staff or rent an office in Germany.",
            "You need faster follow-up across time zones and business cultures.",
        ],
        "deliverables": [
            "Local contact and coordination support for agreed activities",
            "Meeting attendance or support where appropriate",
            "Follow-up handling after events or partner discussions",
            "Relationship notes and opportunity tracking",
            "Monthly or project-based reporting",
        ],
        "process": [
            ("Scope", "We define what local representation means for your case."),
            ("Set up", "We align communication routes, materials and contact rules."),
            ("Operate", "We support agreed market-facing activities from Germany."),
            ("Report", "You keep visibility on conversations, actions and next steps."),
        ],
        "faq": [
            ("Is this a legal representative service?", "TradeGate provides business representation and market support. Regulated legal representation is clarified separately and may require specialist partners."),
            ("Can this replace a German office?", "For early validation and relationship building, it can be a lean alternative before larger commitments."),
            ("Can you receive visitors or attend meetings?", "Yes, subject to scope, location and scheduling."),
        ],
        "related": ["germany-market-entry-support", "trade-fair-follow-up-lead-management", "find-business-partners-germany"],
    },
    "distributor-search-germany": {
        "slug": "distributor-search-germany",
        "service_code": "distributor_search",
        "kicker": "Distributor search Germany",
        "title": "Distributor Search in Germany for Export-Ready Companies",
        "subtitle": "Move beyond generic directories. TradeGate helps identify, prioritize and approach German distributor candidates that match your industry, product and market readiness.",
        "primary_keyword": "distributor search Germany",
        "meta_title": "Distributor Search Germany | TradeGate Consultants",
        "meta_description": "Distributor search in Germany for export-ready SMEs: target profile, shortlist, outreach support and qualification.",
        "hero_badges": ["Export-ready SMEs", "German distributors", "Shortlist", "Outreach support"],
        "pain_points": [
            "Many distributor lists are outdated or too broad.",
            "German distributors expect clear product information and realistic margins.",
            "You need to know who is worth pursuing first.",
        ],
        "deliverables": [
            "Distributor profile and fit criteria",
            "Prioritized candidate list",
            "Outreach script and localized email support",
            "Response tracking and qualification notes",
            "Recommended follow-up sequence",
        ],
        "process": [
            ("Prepare", "We review your product readiness and distributor fit."),
            ("Research", "We build a focused list around industry and channel logic."),
            ("Engage", "We support first approach and follow-up."),
            ("Qualify", "We identify who deserves deeper discussion."),
        ],
        "faq": [
            ("What do you need from us?", "A clear company profile, product details, website or brochure, target margins if available, and market goals."),
            ("Can you help with food, agriculture or manufacturing?", "Yes, those sectors fit the TradeGate positioning well when export readiness is clear."),
            ("Is this the same as sales agency work?", "It can support sales development, but distributor search is usually a defined project with clear deliverables."),
        ],
        "related": ["find-business-partners-germany", "germany-market-entry-support", "trade-fair-representation-germany"],
    },
    "trade-fair-follow-up-lead-management": {
        "slug": "trade-fair-follow-up-lead-management",
        "service_code": "follow_up",
        "kicker": "Lead follow-up Germany",
        "title": "Trade Fair Follow-up and Lead Management in Germany",
        "subtitle": "After a trade fair, speed and structure matter. TradeGate helps organize leads, follow up professionally, and turn event conversations into real business opportunities.",
        "primary_keyword": "trade fair follow-up Germany",
        "meta_title": "Trade Fair Follow-up Germany | TradeGate Consultants",
        "meta_description": "Trade fair lead follow-up and relationship management in Germany: organize leads, qualify interest, send follow-up and prepare next steps.",
        "hero_badges": ["Post-event follow-up", "Lead qualification", "German market", "Next steps"],
        "pain_points": [
            "Many trade fair leads go cold because follow-up is slow or unclear.",
            "Your team may be outside Europe and busy after the event.",
            "You need structured next steps, not a stack of business cards.",
        ],
        "deliverables": [
            "Lead organization and priority tagging",
            "Follow-up email support and response tracking",
            "Meeting scheduling support where agreed",
            "Opportunity notes and recommended next actions",
            "Summary report for management",
        ],
        "process": [
            ("Organize", "We turn raw contacts into a usable lead list."),
            ("Prioritize", "We separate hot prospects, information requests and low-fit contacts."),
            ("Follow up", "We help send timely, professional follow-ups."),
            ("Convert", "We prepare next-step calls, samples, partner talks or proposals."),
        ],
        "faq": [
            ("Can you help after an event we attended ourselves?", "Yes. If you have leads or notes, we can help structure the follow-up process."),
            ("Do you write follow-up emails?", "Yes, depending on the scope we can prepare or support follow-up communication."),
            ("Can this be combined with event representation?", "Yes. The strongest model is representation plus structured follow-up."),
        ],
        "related": ["trade-fair-representation-germany", "eu-local-representative-germany", "find-business-partners-germany"],
    },
}

SERVICE_NAV = [
    ("Trade Fair Representation", "trade-fair-representation-germany"),
    ("Partner Search", "find-business-partners-germany"),
    ("Market Entry Support", "germany-market-entry-support"),
    ("EU Local Presence", "eu-local-representative-germany"),
    ("Distributor Search", "distributor-search-germany"),
    ("Lead Follow-up", "trade-fair-follow-up-lead-management"),
]

DEFAULT_OPPORTUNITIES = [
    {
        "title": "Fruit Logistica Berlin",
        "slug": "fruit-logistica-berlin",
        "city_country": "Berlin, Germany",
        "date_label": "Food export · fresh produce",
        "industry": "Agriculture, food & retail",
        "summary": "A strong entry point for exporters seeking importers, distributors and retail conversations in Europe.",
        "cta_label": "Request representation",
        "cta_url": "/contact/?service=trade_fair&event=fruit-logistica-berlin#contact-form",
        "visual_label": "Berlin",
    },
    {
        "title": "Anuga Cologne",
        "slug": "anuga-cologne",
        "city_country": "Cologne, Germany",
        "date_label": "Food & beverage distribution",
        "industry": "FMCG, ingredients, private label",
        "summary": "Useful for food and beverage producers preparing for German/EU buyers and distribution partners.",
        "cta_label": "Discuss market entry",
        "cta_url": "/contact/?service=scouting&event=anuga-cologne#contact-form",
        "visual_label": "Köln",
    },
    {
        "title": "Hannover Messe",
        "slug": "hannover-messe",
        "city_country": "Hannover, Germany",
        "date_label": "Industry, machinery & technology",
        "industry": "Manufacturing, energy, automation",
        "summary": "Ideal for manufacturers and technology firms seeking visibility, partners and industrial buyers.",
        "cta_label": "Find partners",
        "cta_url": "/contact/?service=scouting&event=hannover-messe#contact-form",
        "visual_label": "HMI",
    },
]


# ---------------------------------------------------------------------------
# Service details and packages (Nov 2026).
# Every service page explains: who it is for, what is included, what you
# receive, how long it takes, what it costs, what we need from you and what
# is not included. Prices are "from" prices; the final quote follows a short
# call, so there is room to adjust scope.
# ---------------------------------------------------------------------------

PRICING_NOTE = (
    "Prices are starting points in euros, net of VAT where it applies. "
    "After a short call we confirm the scope and price in a one-page agreement. "
    "Work starts only once the agreement is signed."
)

SERVICE_DETAILS = {
    "trade-fair-representation-germany": {
        "card_summary": "We attend a German or EU trade fair for you, meet the visitors you want and send you the leads and a report.",
        "from_price": "From €650 per fair day",
        "who_for": "Export-ready companies that want to be seen at a German or EU trade fair without sending their own team.",
        "timeline": "Book at least 3 weeks before the fair. The report arrives within 3 working days after the last fair day.",
        "we_need": [
            "Your company profile, product sheets and price list",
            "The kind of buyers you want to meet",
            "Your booth details, if you have a booth",
            "Samples or brochures, if you want them handed out",
        ],
        "not_included": [
            "Fair tickets, travel and hotel (charged at cost, agreed in advance)",
            "Booth rental and booth construction",
            "Signing contracts on your behalf",
        ],
        "packages": [
            {
                "name": "Fair day",
                "price": "From €650",
                "unit": "per fair day + ticket and travel at cost",
                "best_for": "One fair, one clear goal",
                "includes": [
                    "Pre-fair briefing call",
                    "Attendance or booth support for one day",
                    "Lead list with notes",
                    "Photos and a short written report",
                ],
            },
            {
                "name": "Fair + follow-up",
                "price": "From €950",
                "unit": "per fair day + ticket and travel at cost",
                "best_for": "Turning fair contacts into meetings",
                "featured": True,
                "includes": [
                    "Everything in Fair day",
                    "Follow-up of every lead for 3 weeks",
                    "Booking of first calls or meetings",
                    "Final summary with next steps",
                ],
            },
            {
                "name": "Multi-day or booth staffing",
                "price": "By quote",
                "unit": "",
                "best_for": "Several days, several fairs or a full booth",
                "includes": [
                    "Scope agreed on a call",
                    "Daily reporting during the fair",
                    "Follow-up included",
                ],
            },
        ],
    },
    "find-business-partners-germany": {
        "card_summary": "We find and check potential partners in Germany, contact the best ones and set up the first calls.",
        "from_price": "From €490",
        "who_for": "Companies looking for importers, resellers, sourcing partners or other business partners in Germany.",
        "timeline": "Shortlist in 2 weeks. Outreach and first calls within 6 weeks.",
        "we_need": [
            "Your product or service, prices and minimum order quantities",
            "The partner profile you want (type, size, region)",
            "Certifications and export documents you already have",
        ],
        "not_included": [
            "Guaranteed deals or sales",
            "Legal, tax or customs advice",
            "Translation of your full catalogue",
        ],
        "packages": [
            {
                "name": "Partner shortlist",
                "price": "€490",
                "unit": "one-off",
                "best_for": "Seeing who is out there before you invest more",
                "includes": [
                    "30 checked potential partners",
                    "Why each one fits, plus contact routes",
                    "Short market notes",
                ],
            },
            {
                "name": "Shortlist + outreach",
                "price": "From €890",
                "unit": "+ €1,200 per signed partner",
                "best_for": "Getting real conversations started",
                "featured": True,
                "includes": [
                    "Everything in Partner shortlist",
                    "Personal outreach to the best 15",
                    "Reply tracking and follow-up",
                    "First introduction calls set up",
                ],
            },
            {
                "name": "Custom search",
                "price": "By quote",
                "unit": "",
                "best_for": "Several sectors, countries or partner types",
                "includes": [
                    "Scope agreed on a call",
                    "Regular progress updates",
                ],
            },
        ],
    },
    "germany-market-entry-support": {
        "card_summary": "We check how your offer fits Germany and give you a clear first route: which fair, which partners, which price level.",
        "from_price": "From €390",
        "who_for": "Companies that want to enter Germany but are not yet sure where to start.",
        "timeline": "Entry check in 1 week. Entry plan with first contacts in 4 weeks.",
        "we_need": [
            "Your product range, prices and current export markets",
            "Your goal for Germany and your budget range",
        ],
        "not_included": [
            "Company registration or legal set-up in Germany",
            "Product certification or labelling work",
        ],
        "packages": [
            {
                "name": "Entry check",
                "price": "€390",
                "unit": "one-off",
                "best_for": "A fast, honest first view",
                "includes": [
                    "60-minute call",
                    "Written one-page entry route",
                    "Price and positioning notes",
                    "Recommended first fair or partner route",
                ],
            },
            {
                "name": "Entry plan + first contacts",
                "price": "From €990",
                "unit": "one-off",
                "best_for": "Starting with real contacts",
                "featured": True,
                "includes": [
                    "Everything in Entry check",
                    "Market and competitor snapshot",
                    "Shortlist of 20 first contacts",
                    "Personal outreach to the best 10",
                ],
            },
            {
                "name": "Ongoing support",
                "price": "From €290",
                "unit": "per month, after a first project",
                "best_for": "Keeping momentum after the first results",
                "includes": [
                    "Monthly priorities and follow-up",
                    "Monthly progress report",
                ],
            },
        ],
    },
    "eu-local-representative-germany": {
        "card_summary": "A named contact person in Germany who answers your partners, attends meetings and keeps relationships going.",
        "from_price": "From €290 per month",
        "who_for": "Companies with first German contacts that need someone local before opening an office.",
        "timeline": "Starts within 2 weeks of signing. Minimum term 3 months.",
        "we_need": [
            "Your key contacts and open conversations",
            "Clear rules on what we may say and promise on your behalf",
        ],
        "not_included": [
            "A registered office address or virtual office",
            "Signing contracts on your behalf",
            "Travel outside Leipzig (charged at cost, agreed in advance)",
        ],
        "packages": [
            {
                "name": "Local contact",
                "price": "From €290",
                "unit": "per month, minimum 3 months",
                "best_for": "Being reachable in Germany",
                "includes": [
                    "Named contact person in Germany",
                    "Answers to partner enquiries in German and English",
                    "Monthly update",
                ],
            },
            {
                "name": "Local contact + meetings",
                "price": "From €490",
                "unit": "per month, minimum 3 months",
                "best_for": "Active relationship building",
                "featured": True,
                "includes": [
                    "Everything in Local contact",
                    "Up to 2 meetings a month",
                    "Follow-up management",
                ],
            },
        ],
    },
    "distributor-search-germany": {
        "card_summary": "We find German distributors that match your product, contact them and set up the first talks.",
        "from_price": "From €490",
        "who_for": "Manufacturers and exporters looking for distributors or wholesalers in Germany.",
        "timeline": "Shortlist in 2 weeks. Outreach and first talks within 6 weeks.",
        "we_need": [
            "Product details, prices and minimum order quantities",
            "Packaging, shelf life and certifications",
            "Delivery terms you can offer (for example EXW or CIF)",
        ],
        "not_included": [
            "Guaranteed distribution agreements",
            "Logistics, customs clearance or warehousing",
        ],
        "packages": [
            {
                "name": "Distributor shortlist",
                "price": "€490",
                "unit": "one-off",
                "best_for": "Knowing which distributors fit",
                "includes": [
                    "25 checked distributor candidates",
                    "Why each one fits, plus contact routes",
                    "Notes on what they usually expect",
                ],
            },
            {
                "name": "Shortlist + outreach",
                "price": "From €890",
                "unit": "+ €1,200 per signed distributor",
                "best_for": "Getting distributor talks started",
                "featured": True,
                "includes": [
                    "Everything in Distributor shortlist",
                    "Personal outreach to the best 12",
                    "Sample and price-list follow-up",
                    "First talks set up",
                ],
            },
            {
                "name": "Custom search",
                "price": "By quote",
                "unit": "",
                "best_for": "Several product lines or EU countries",
                "includes": [
                    "Scope agreed on a call",
                    "Regular progress updates",
                ],
            },
        ],
    },
    "trade-fair-follow-up-lead-management": {
        "card_summary": "After a fair, we follow up every contact you collected and turn the interested ones into calls.",
        "from_price": "From €350",
        "who_for": "Companies that came back from a fair with contacts but no time to follow up.",
        "timeline": "Starts within 1 week. Each sprint runs 4 weeks.",
        "we_need": [
            "Your lead list, business cards or scanner export",
            "Your notes from the fair, if you have them",
            "Your offer, prices and what you want from each lead",
        ],
        "not_included": [
            "Sales negotiations on your behalf",
            "Leads you did not collect yourself",
        ],
        "packages": [
            {
                "name": "Follow-up sprint",
                "price": "€350",
                "unit": "up to 50 leads, 4 weeks",
                "best_for": "Not losing contacts after a fair",
                "includes": [
                    "Lead list cleaned and ranked",
                    "Personal follow-up of every lead",
                    "Reply tracking",
                    "Summary of who is interested",
                ],
            },
            {
                "name": "Follow-up + meetings",
                "price": "From €590",
                "unit": "up to 100 leads, 4 weeks",
                "best_for": "Turning interest into calls",
                "featured": True,
                "includes": [
                    "Everything in Follow-up sprint",
                    "Calls or meetings booked",
                    "Next-step notes for each hot lead",
                ],
            },
        ],
    },
}

for _slug, _details in SERVICE_DETAILS.items():
    SERVICE_PAGES[_slug].update(_details)


# Service for trade-fair organisers (separate audience, commission only).
SERVICE_PAGES["exhibitor-recruitment-germany"] = {
    "slug": "exhibitor-recruitment-germany",
    "service_code": "exhibitor_recruitment",
    "audience": "organisers",
    "kicker": "For trade-fair organisers",
    "title": "Exhibitor Recruitment in Germany for International Trade Fairs",
    "subtitle": "Organising a trade fair abroad and looking for German exhibitors? TradeGate acts as your agent for Germany: we find suitable companies, introduce your event and follow up until they book.",
    "primary_keyword": "exhibitor recruitment Germany",
    "meta_title": "Exhibitor Recruitment Germany | TradeGate Consultants",
    "meta_description": "Germany-based exhibitor recruitment agent for international trade fairs: research, introductions and follow-up, paid by commission on confirmed bookings.",
    "hero_badges": ["Commission only", "Germany-based", "Lead registration", "Monthly reporting"],
    "card_summary": "For organisers of trade fairs abroad: we recruit German exhibitors and sponsors for your event, paid by commission.",
    "from_price": "Commission on confirmed bookings",
    "who_for": "Organisers of international trade fairs and expos who want exhibitors or sponsors from Germany.",
    "pain_points": [
        "German companies rarely respond to foreign event marketing they have never heard of.",
        "You need someone who knows which German companies fit your sectors.",
        "You want to pay for results, not for activity.",
    ],
    "deliverables": [
        "Research of German companies that fit your sectors",
        "Introduction of your event in German and English",
        "Registration of every introduced company with you",
        "Follow-up until the company books or declines",
        "Monthly report on contacts, interest and bookings",
    ],
    "process": [
        ("Agree", "We review your event, packages and terms and sign an agent agreement."),
        ("Register", "We register each company with you before we introduce your event."),
        ("Recruit", "We introduce the event, answer questions and follow up."),
        ("Report", "You get a monthly report; commission is due once a booking is paid."),
    ],
    "timeline": "Best started 6 to 9 months before the event, so German companies can plan their budget.",
    "we_need": [
        "Event presentation, exhibitor and sponsorship packages with prices",
        "Results from previous editions",
        "Proof of the contracting company and the venue",
        "Written permission to use your event name and logo",
    ],
    "not_included": [
        "Upfront fees",
        "Travel to the event (agreed separately if needed)",
        "Paid advertising campaigns",
    ],
    "commission_terms": [
        "Commission on all confirmed and fully paid business from companies we introduced: booth space, sponsorship, advertising and upgrades",
        "Rate agreed per event",
        "Registered companies stay protected for this edition and the next",
        "Payment within 30 days after you receive the exhibitor's payment, with a monthly statement",
    ],
    "faq": [
        ("Do you charge an upfront fee?", "No. We work on commission on confirmed and fully paid bookings."),
        ("How do you avoid disputes about who introduced a company?", "We register every company with you in writing before we contact it, and you confirm the registration."),
        ("Which sectors do you cover?", "Mainly food and agriculture, machinery and technology, and consumer sectors. We confirm fit after reviewing your event."),
    ],
    "related": ["trade-fair-representation-germany", "find-business-partners-germany"],
}

ORGANISER_NAV = [
    ("Exhibitor Recruitment (for organisers)", "exhibitor-recruitment-germany"),
]


# Founder section on the About page. Photo, LinkedIn and background are
# shown only once they are filled in.
FOUNDER = {
    "name": "Ivan Nkomati",
    "role": "Founder & Managing Partner",
    "location": "Leipzig, Germany",
    "photo_url": "/static/website/img/ivan-nkomati.webp",
    "linkedin_url": "https://www.linkedin.com/in/ivan-nkomati-313637228",
    "background": "",     # two or three sentences, to be supplied
    "partners": "When a project needs more hands or specialist knowledge, I bring in independent partners, for example trade-fair staff, translators or legal and tax advisers in Germany. I choose them for each project's scope, and you keep one contact: me.",
    "intro": "You work with me directly, from the first call to the final report. TradeGate is run from Leipzig, in German and English.",
}
