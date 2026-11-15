"""Partner pool: reference lists and the rule-based matching engine.

Matching is deliberately simple and explainable. Every suggestion carries the
reasons it was made, and nothing is ever sent to companies automatically: the
owner reviews suggestions in the admin and makes the introduction personally.
"""
import re

# Regions used for "where are you" and "where do you look for partners".
REGION_CHOICES = [
    ("germany", "Germany"),
    ("dach", "Austria and Switzerland"),
    ("eu", "Rest of the EU"),
    ("europe_other", "Rest of Europe (incl. UK and Türkiye)"),
    ("africa", "Africa"),
    ("middle_east", "Middle East"),
    ("asia", "Asia"),
    ("americas", "Americas"),
    ("oceania", "Oceania"),
]
TARGET_CHOICES = REGION_CHOICES + [("any", "Open to any region")]

COUNTRIES_BY_REGION = {
    "germany": ["Germany"],
    "dach": ["Austria", "Switzerland", "Liechtenstein"],
    "eu": [
        "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czechia", "Denmark", "Estonia", "Finland",
        "France", "Greece", "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg",
        "Malta", "Netherlands", "Poland", "Portugal", "Romania", "Slovakia", "Slovenia", "Spain", "Sweden",
    ],
    "europe_other": [
        "Albania", "Andorra", "Belarus", "Bosnia and Herzegovina", "Iceland", "Kosovo", "Moldova",
        "Monaco", "Montenegro", "North Macedonia", "Norway", "San Marino", "Serbia", "Türkiye",
        "Ukraine", "United Kingdom",
    ],
    "africa": [
        "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cabo Verde", "Cameroon",
        "Central African Republic", "Chad", "Comoros", "Congo (Brazzaville)", "Congo (DRC)", "Côte d'Ivoire",
        "Djibouti", "Egypt", "Equatorial Guinea", "Eritrea", "Eswatini", "Ethiopia", "Gabon", "Gambia",
        "Ghana", "Guinea", "Guinea-Bissau", "Kenya", "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi",
        "Mali", "Mauritania", "Mauritius", "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda",
        "São Tomé and Príncipe", "Senegal", "Seychelles", "Sierra Leone", "Somalia", "South Africa",
        "South Sudan", "Sudan", "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe",
    ],
    "middle_east": [
        "Bahrain", "Iran", "Iraq", "Israel", "Jordan", "Kuwait", "Lebanon", "Oman", "Palestine", "Qatar",
        "Saudi Arabia", "Syria", "United Arab Emirates", "Yemen",
    ],
    "asia": [
        "Afghanistan", "Armenia", "Azerbaijan", "Bangladesh", "Bhutan", "Brunei", "Cambodia", "China",
        "Georgia", "Hong Kong", "India", "Indonesia", "Japan", "Kazakhstan", "Kyrgyzstan", "Laos", "Malaysia",
        "Maldives", "Mongolia", "Myanmar", "Nepal", "Pakistan", "Philippines", "Singapore", "South Korea",
        "Sri Lanka", "Taiwan", "Tajikistan", "Thailand", "Timor-Leste", "Turkmenistan", "Uzbekistan", "Vietnam",
    ],
    "americas": [
        "Argentina", "Bahamas", "Barbados", "Belize", "Bolivia", "Brazil", "Canada", "Chile", "Colombia",
        "Costa Rica", "Cuba", "Dominican Republic", "Ecuador", "El Salvador", "Guatemala", "Guyana", "Haiti",
        "Honduras", "Jamaica", "Mexico", "Nicaragua", "Panama", "Paraguay", "Peru", "Suriname",
        "Trinidad and Tobago", "United States", "Uruguay", "Venezuela",
    ],
    "oceania": ["Australia", "Fiji", "New Zealand", "Papua New Guinea", "Samoa", "Solomon Islands", "Tonga", "Vanuatu"],
}
REGION_OF_COUNTRY = {c: r for r, cs in COUNTRIES_BY_REGION.items() for c in cs}
COUNTRY_CHOICES = [("", "Select country")] + sorted(((c, c) for c in REGION_OF_COUNTRY), key=lambda x: x[0])

SECTOR_CHOICES = [
    ("", "Select sector"),
    ("agrifood", "Agriculture, food and beverages"),
    ("automotive", "Automotive and mobility"),
    ("chemicals", "Chemicals and plastics"),
    ("construction", "Construction and building materials"),
    ("consumer", "Consumer goods and retail"),
    ("energy", "Energy and renewables"),
    ("fashion", "Textiles, fashion and leather"),
    ("health", "Healthcare, medical and pharma"),
    ("ict", "IT, software and electronics"),
    ("logistics", "Logistics and transport"),
    ("machinery", "Machinery and industrial equipment"),
    ("mining", "Mining, metals and raw materials"),
    ("services", "Business and professional services"),
    ("tourism", "Tourism and hospitality"),
    ("wood", "Wood, furniture and paper"),
    ("other", "Other"),
]

COMPANY_TYPE_CHOICES = [
    ("", "Select type"),
    ("manufacturer", "Manufacturer / producer"),
    ("exporter", "Exporter / trading company"),
    ("distributor", "Importer / distributor / wholesaler"),
    ("retailer", "Retailer / e-commerce"),
    ("service", "Service provider"),
    ("investor", "Investor"),
    ("other", "Other"),
]

PARTNER_TYPE_CHOICES = [
    ("distributor", "Importer / distributor"),
    ("supplier", "Supplier / manufacturer"),
    ("agent", "Sales agent / representative"),
    ("buyer", "Buyer / retailer"),
    ("jv", "Joint venture / investor"),
    ("service", "Service or technology partner"),
]

SIZE_CHOICES = [
    ("", "Select size"),
    ("1_9", "1–9 employees"),
    ("10_49", "10–49 employees"),
    ("50_249", "50–249 employees"),
    ("250_plus", "250+ employees"),
]

# Which company types fulfil which sought partner type.
FULFILS = {
    "distributor": {"distributor"},
    "supplier": {"manufacturer", "exporter"},
    "agent": {"service", "distributor", "other"},
    "buyer": {"retailer", "distributor"},
    "jv": {"investor", "manufacturer"},
    "service": {"service"},
}

STOPWORDS = set(
    "a an and are as at be by for from in into is of on or our the to we with you your us it its "
    "products product services service company companies business partner partners looking seek seeking "
    "offer offers germany german europe eu market markets international quality high new also all any "
    "der die das und für mit von wir ein eine im in zu auf".split()
)


def region_of(country):
    return REGION_OF_COUNTRY.get(country or "", "")


def split_csv(value):
    return [v for v in (value or "").split(",") if v]


def keywords(*texts):
    words = set()
    for t in texts:
        for w in re.findall(r"[a-zA-ZÀ-ÿ]{4,}", (t or "").lower()):
            if w not in STOPWORDS:
                words.add(w[:-1] if w.endswith("s") and len(w) > 4 else w)
    return words


def _targets(profile, other):
    targets = set(split_csv(profile.target_regions))
    return "any" in targets or region_of(other.country) in targets


def score(a, b):
    """Score how well b fits what a is looking for. Returns (score, reasons)."""
    if a.pk and b.pk and a.pk == b.pk:
        return 0, []
    if a.email and b.email and a.email.lower() == b.email.lower():
        return 0, []
    if not (_targets(a, b) and _targets(b, a)):
        return 0, []

    points, reasons = 0, []
    if a.sector and a.sector == b.sector and a.sector != "other":
        points += 40
        reasons.append("same sector")

    sought = set(split_csv(a.partner_types))
    if b.company_type and any(b.company_type in FULFILS.get(s, set()) for s in sought):
        points += 25
        reasons.append(f"{b.get_company_type_display().lower()} fits what they seek")
    sought_b = set(split_csv(b.partner_types))
    if a.company_type and any(a.company_type in FULFILS.get(s, set()) for s in sought_b):
        points += 10
        reasons.append("they fit what the other seeks too")

    shared = keywords(a.seeking, a.products) & keywords(b.offering, b.products)
    if shared:
        points += min(25, 5 * len(shared))
        reasons.append("shared terms: " + ", ".join(sorted(shared)[:5]))

    # A match needs real substance: same sector, or clear overlap in what is sought and offered.
    if "same sector" not in reasons and len(shared) < 2:
        return 0, []
    reasons.insert(0, "regions fit both ways")
    return min(points, 100), reasons


def suggestions_for(profile, candidates, limit=10, minimum=40):
    out = []
    for other in candidates:
        s1, r1 = score(profile, other)
        if not s1:
            continue
        s2, _ = score(other, profile)
        total = round(s1 * 0.7 + s2 * 0.3)
        if total >= minimum:
            out.append((total, other, r1))
    out.sort(key=lambda x: -x[0])
    return out[:limit]


# Confirmation email sent to a company after it registers (only when switched on
# in Site Settings). Written in the language the company used on the website.
CONFIRMATION = {
    "en": ("Your company is registered in the TradeGate Partner Hub",
           "Dear {name},\n\n"
           "thank you for registering {company} in the TradeGate Partner Hub.\n\n"
           "What happens next:\n"
           "1. We review your profile within 2 working days.\n"
           "2. We compare it with the companies in our network.\n"
           "3. When we see a fitting partner, we contact you first. We only make an introduction when both sides agree.\n\n"
           "Your profile is private. We never publish it or pass on your details without your approval.\n\n"
           "Your summary:\n{summary}\n\n"
           "To update or delete your profile, simply reply to this email.\n\n"
           "Kind regards\nTradeGate Consultants\nwww.tradegateconsultants.com"),
    "de": ("Ihr Unternehmen ist im TradeGate Partner Hub registriert",
           "Guten Tag {name},\n\n"
           "vielen Dank, dass Sie {company} im TradeGate Partner Hub registriert haben.\n\n"
           "So geht es weiter:\n"
           "1. Wir prüfen Ihr Profil innerhalb von 2 Werktagen.\n"
           "2. Wir gleichen es mit den Unternehmen in unserem Netzwerk ab.\n"
           "3. Sehen wir einen passenden Partner, melden wir uns zuerst bei Ihnen. Wir stellen nur vor, wenn beide Seiten zustimmen.\n\n"
           "Ihr Profil ist privat. Wir veröffentlichen es nie und geben Ihre Daten nicht ohne Ihre Zustimmung weiter.\n\n"
           "Ihre Angaben im Überblick:\n{summary}\n\n"
           "Um Ihr Profil zu ändern oder zu löschen, antworten Sie einfach auf diese E-Mail.\n\n"
           "Mit freundlichen Grüßen\nTradeGate Consultants\nwww.tradegateconsultants.com"),
    "fr": ("Votre entreprise est inscrite au TradeGate Partner Hub",
           "Bonjour {name},\n\n"
           "merci d’avoir inscrit {company} au TradeGate Partner Hub.\n\n"
           "Les prochaines étapes :\n"
           "1. Nous examinons votre profil sous 2 jours ouvrés.\n"
           "2. Nous le comparons avec les entreprises de notre réseau.\n"
           "3. Dès que nous voyons un partenaire adapté, nous vous contactons d’abord. Nous ne faisons de mise en relation qu’avec l’accord des deux parties.\n\n"
           "Votre profil est privé. Nous ne le publions jamais et ne transmettons pas vos coordonnées sans votre accord.\n\n"
           "Votre résumé :\n{summary}\n\n"
           "Pour modifier ou supprimer votre profil, répondez simplement à cet e-mail.\n\n"
           "Cordialement\nTradeGate Consultants\nwww.tradegateconsultants.com"),
    "pt": ("A sua empresa está registada no TradeGate Partner Hub",
           "Olá {name},\n\n"
           "obrigado por registar {company} no TradeGate Partner Hub.\n\n"
           "Próximos passos:\n"
           "1. Analisamos o seu perfil no prazo de 2 dias úteis.\n"
           "2. Comparamo-lo com as empresas da nossa rede.\n"
           "3. Quando virmos um parceiro adequado, contactamo-lo primeiro. Só fazemos uma apresentação com o acordo de ambas as partes.\n\n"
           "O seu perfil é privado. Nunca o publicamos nem partilhamos os seus dados sem a sua autorização.\n\n"
           "O seu resumo:\n{summary}\n\n"
           "Para atualizar ou eliminar o seu perfil, basta responder a este e-mail.\n\n"
           "Com os melhores cumprimentos\nTradeGate Consultants\nwww.tradegateconsultants.com"),
    "es": ("Su empresa está registrada en el TradeGate Partner Hub",
           "Hola {name}:\n\n"
           "gracias por registrar {company} en el TradeGate Partner Hub.\n\n"
           "Próximos pasos:\n"
           "1. Revisamos su perfil en un plazo de 2 días laborables.\n"
           "2. Lo comparamos con las empresas de nuestra red.\n"
           "3. Cuando veamos un socio adecuado, le contactamos primero a usted. Solo hacemos una presentación con el acuerdo de ambas partes.\n\n"
           "Su perfil es privado. Nunca lo publicamos ni compartimos sus datos sin su aprobación.\n\n"
           "Su resumen:\n{summary}\n\n"
           "Para actualizar o eliminar su perfil, simplemente responda a este correo.\n\n"
           "Saludos cordiales\nTradeGate Consultants\nwww.tradegateconsultants.com"),
}


def confirmation_email(profile):
    """(subject, body) for the company, in the language it registered in."""
    subject, body = CONFIRMATION.get(profile.language or "en", CONFIRMATION["en"])
    summary = "\n".join([
        f"- {profile.company_name}, {profile.country}",
        f"- {profile.products}",
        f"- {', '.join(profile.partner_type_labels())}",
    ])
    return subject, body.format(name=profile.contact_name, company=profile.company_name, summary=summary)
