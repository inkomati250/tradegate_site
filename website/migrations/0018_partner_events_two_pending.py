"""
Partner events: keep only the two events whose agreements are being finalised
(ECOWAS Aviana, Azerbaijan Mining Expo), give them full descriptions, the
organisers' published prices and their logos. The Women Expo entries are removed
if they were never published. Everything stays editable in the admin, and the
partner events stay hidden until 'materials permission' and 'published' are ticked.
"""
from datetime import date
from pathlib import Path

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import migrations

SEED_DIR = Path(__file__).resolve().parent.parent / "seed" / "trade-fairs" / "logos"

HELP = """We explain the event, the hall options and the packages in English or German
We check that the event fits your products and the buyers you want to meet
We register you with the organiser and help with the booking and paperwork
We stay your point of contact before, during and after the event"""

AVIANA = dict(
    slug="ecowas-aviana-expo-2027",
    name="ECOWAS Aviana West Africa International Expo 2027",
    start_date=date(2027, 6, 22), end_date=date(2027, 6, 24),
    city="Ibadan", country="Nigeria",
    venue="University of Ibadan International Conference Centre",
    organiser="ECOWAS Aviana Expo (Nigeria)",
    sectors="Poultry, Livestock, Animal feed, Veterinary, Agricultural machinery, AgriTech, Aquaculture, Dairy, Food processing, Seeds, Fertiliser",
    summary="West Africa's meeting point for poultry, livestock, feed and agricultural technology: three days in Ibadan with producers, buyers and distributors from across the ECOWAS region.",
    description=(
        "Nigeria is the largest agricultural market in West Africa, and demand for better feed, "
        "animal health, mechanisation and processing keeps growing. The ECOWAS Aviana West Africa "
        "International Expo brings that demand into one hall. Farmers, integrated poultry and livestock "
        "producers, feed millers, processors, cooperatives, distributors and public agencies come to Ibadan "
        "to see new products, compare suppliers and meet partners. For suppliers from Germany, the EU and "
        "elsewhere it is a practical way to test the market, meet importers and distributors face to face "
        "and build a network in the region, without opening an office first."
    ),
    who_should_exhibit=(
        "Agricultural machinery, tractors and equipment makers\n"
        "AgriTech, precision farming and farm software companies\n"
        "Animal health, veterinary and feed additive suppliers\n"
        "Feed milling, poultry housing and hatchery equipment suppliers\n"
        "Seed, fertiliser and crop input companies\n"
        "Food processing, dairy and packaging technology suppliers\n"
        "Aquaculture equipment and feed companies"
    ),
    who_should_visit=(
        "Companies looking for importers and distributors in Nigeria and West Africa\n"
        "Exporters researching agricultural demand in the ECOWAS region\n"
        "Investors and development partners in African agribusiness"
    ),
    how_we_help=HELP,
    our_role="Exhibitor recruitment partner (non-exclusive)",
    official_url="https://ecowasavianavivexpo.com/",
    packages_text=(
        "Built-up stand, 9 m² | US$ 2,650 | Halls B, C, E and Gallery (Hall A: US$ 2,800). Table, two chairs, power point, name on fascia, full-page advert and logo in the catalogue\n"
        "Built-up stand, 12 m² | US$ 3,600 | Halls B, C, E and Gallery (Hall A: US$ 3,810). Table, three chairs, power point, fascia name, full-page advert, catalogue logo\n"
        "Built-up stand, 18 m² | US$ 5,300 | Halls B, C, E and Gallery (Hall A: US$ 5,600). Two tables, six chairs, two power points, fascia name, full-page advert, catalogue logo\n"
        "Product presentation | US$ 1,300 | One hour on the conference programme\n"
        "Catalogue advertising | from US$ 370 | Quarter page US$ 370, half page US$ 485, full page US$ 910, covers up to US$ 1,810\n"
        "Sponsorship packages | US$ 9,500 – 18,500 | Bronze, Silver, Gold, Diamond and Platinum: includes free stand space, advert, product presentation, logo on all materials and media publicity\n"
        "Branding options | from US$ 1,820 | Registration area, lanyards, bags and folders, T-shirts and caps, catering"
    ),
    packages_note="Organiser's 2027 prices for international exhibitors, in US dollars. Our fee is paid by the organiser, so booking through us does not add to your price.",
    logo_file="ecowas-aviana-expo.webp",
)

AME = dict(
    slug="azerbaijan-mining-expo-2027",
    name="Azerbaijan Mining Expo 2027",
    start_date=date(2027, 9, 8), end_date=date(2027, 9, 10),
    city="Baku", country="Azerbaijan",
    venue="Baku Expo Center",
    organiser="Intro Exhibition & Conference and True Expo",
    sectors="Mining, Mineral processing, Heavy equipment, Construction machinery, Drilling, Automation, Mine safety, Metallurgy",
    summary="The international mining, heavy equipment and construction machinery exhibition in Baku, as Azerbaijan starts a new programme of gold, copper and iron projects.",
    description=(
        "Azerbaijan has launched a 2027–2030 state programme to develop its gold, copper, iron and "
        "polymetallic deposits and to process more of its ore at home, with new mines, beneficiation "
        "plants and metallurgy capacity planned. Azerbaijan Mining Expo is where the companies behind "
        "these projects meet their suppliers. Now merged with the Caspian Mining Expo into one event, it "
        "brings mining companies, contractors, engineers, government delegations and buyers from "
        "Azerbaijan and the wider Caspian and Central Asian region to Baku for three days, with an "
        "exhibition, a conference programme and dedicated networking areas. For equipment and "
        "technology suppliers it is an early chance to be known before the big contracts are awarded."
    ),
    who_should_exhibit=(
        "Mining machinery, haulage and earth-moving equipment makers\n"
        "Crushing, screening, grinding and mineral processing suppliers\n"
        "Drilling, exploration and blasting technology companies\n"
        "Conveyor, pump, valve and hydraulic component suppliers\n"
        "Automation, sensors, software and Mining 4.0 providers\n"
        "Mine safety, ventilation, dust control and environmental service companies\n"
        "Engineering, consulting and construction contractors"
    ),
    who_should_visit=(
        "Suppliers researching the Azerbaijani and Caspian mining market\n"
        "Companies looking for local partners and agents in the region\n"
        "Investors following the 2027–2030 mining programme"
    ),
    how_we_help=HELP,
    our_role="Exhibitor recruitment partner (non-exclusive)",
    official_url="https://azerbaijanminingexpo.com/",
    packages_text=(
        "Space only, indoor | €480 per m² | Raw floor space for your own stand builder. Plus €495 administration fee\n"
        "Space only, outdoor | €195 per m² | For machinery and vehicles. Plus €495 administration fee\n"
        "Standard stand | €540 per m² | Walls, carpet, info desk, table, chairs, power outlets, country flag, set-up and dismantling. Plus €495 administration fee\n"
        "Premium stand | €660 per m² | Branded stand with furniture, LED lighting, smart TV and digital printing. Plus €495 administration fee\n"
        "Show-ready stand | €795 per m² | Custom-designed stand with furniture, LED lighting, smart TV and creative build. Plus €495 administration fee\n"
        "Sponsorship and branding | from €1,250 | From plaza flags and digital cubes to keynote theatre and title sponsorship"
    ),
    packages_note="Organiser's 2027 prices in euros, before any applicable taxes. Our fee is paid by the organiser, so booking through us does not add to your price.",
    logo_file="azerbaijan-mining-expo.webp",
)

REMOVE = ["women-expo-ras-al-khaimah-2027", "women-expo-al-khobar-2027"]


def forwards(apps, schema_editor):
    TradeFair = apps.get_model("website", "TradeFair")
    TradeFair.objects.filter(slug__in=REMOVE, is_published=False).delete()
    for order, data in enumerate([AVIANA, AME]):
        data = dict(data)
        logo_file = data.pop("logo_file")
        slug = data.pop("slug")
        fair, _ = TradeFair.objects.get_or_create(
            slug=slug, defaults={"name": data["name"], "kind": "represented", "summary": data["summary"]}
        )
        for key, value in data.items():
            setattr(fair, key, value)
        fair.kind = "represented"
        fair.order = order
        if not fair.logo:
            source = SEED_DIR / logo_file
            if source.exists():
                name = f"trade-fairs/logos/{logo_file}"
                if not default_storage.exists(name):
                    name = default_storage.save(name, ContentFile(source.read_bytes()))
                fair.logo = name
        fair.save()


class Migration(migrations.Migration):
    dependencies = [("website", "0017_tradefair_packages_image")]
    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
