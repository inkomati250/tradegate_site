from datetime import date

from django.db import migrations

HELP_GERMANY = """We attend for you and meet the buyers you choose, without your team travelling
We pre-book meetings with German importers, distributors and wholesalers before the fair
We collect leads, notes and photos and send you a written report
We follow up every contact after the fair and set up first calls"""

HELP_REPRESENTED = """We explain the event, the packages and the costs in German or English
We check that the event fits your products and target buyers
We register you with the organiser and help with the booking
We stay your contact in Germany before and after the event"""

GERMANY = [
    dict(name="Grüne Woche", slug="gruene-woche-berlin-2027", start=date(2027, 1, 15), end=date(2027, 1, 24),
         city="Berlin", venue="Messe Berlin", organiser="Messe Berlin",
         sectors="Food, Agriculture, Horticulture, Country pavilions",
         summary="Ten-day showcase for food, farming and gardening, with large country pavilions and both trade and public visitors.",
         description="One of the oldest and largest food and agriculture shows in the world. Many countries present their food products in national pavilions, which makes it a strong stage for export promotion agencies and producers who want visibility with German consumers and the trade at the same time.",
         exhibit="Food and drink producers looking for German consumer and retail exposure\nNational and regional export promotion agencies\nAgricultural cooperatives and associations",
         visit="Exporters who want to see how products are presented to German consumers\nAgencies planning a country pavilion",
         url="https://www.gruenewoche.de/en"),
    dict(name="Ambiente", slug="ambiente-frankfurt-2027", start=date(2027, 1, 29), end=date(2027, 2, 2),
         city="Frankfurt am Main", venue="Messe Frankfurt", organiser="Messe Frankfurt",
         sectors="Consumer goods, Home and living, Tableware, Gifts, Interior design",
         summary="Major consumer-goods fair for home, dining, gifts and interior products, with buyers from retail and hospitality.",
         description="A leading meeting point for manufacturers of household goods, tableware, decoration and gift items and the retailers, hotel groups and interior designers who buy them.",
         exhibit="Makers of homeware, ceramics, textiles, crafts and decoration\nGift and lifestyle brands looking for European retailers",
         visit="Exporters researching European design trends and price points\nCompanies looking for importers in the home sector",
         url="https://ambiente.messefrankfurt.com/frankfurt/en.html"),
    dict(name="ISM", slug="ism-cologne-2027", start=date(2027, 1, 31), end=date(2027, 2, 3),
         city="Cologne", venue="Koelnmesse", organiser="Koelnmesse",
         sectors="Sweets, Snacks, Ingredients, Food processing",
         summary="The global meeting point for sweets and snacks, with separate areas for ingredients and manufacturing.",
         description="Brings together producers of chocolate, confectionery, biscuits and savoury snacks with retail buyers, importers and private-label customers. Ingredient suppliers and production technology have their own areas under the same roof.",
         exhibit="Snack and confectionery brands\nSuppliers of cocoa, nuts, dried fruit and other ingredients\nPrivate-label manufacturers",
         visit="Exporters of snack ingredients looking for European processors\nProducers studying packaging and private-label demand",
         url="https://www.ism-cologne.com"),
    dict(name="Fruit Logistica", slug="fruit-logistica-berlin-2027", start=date(2027, 2, 3), end=date(2027, 2, 5),
         city="Berlin", venue="Messe Berlin", organiser="Messe Berlin",
         sectors="Fresh fruit and vegetables, Logistics, Packaging, Agriculture",
         summary="The leading trade fair for the fresh produce business, from growers and packers to importers and retail buyers.",
         description="Covers the whole fresh produce chain: growers, exporters, importers, logistics, packaging and technology. Many importers and supermarket buyers attend, which makes it a key date for fruit and vegetable exporters from Africa, the Middle East and Asia.",
         exhibit="Fresh produce exporters and grower groups\nPack houses and cold-chain providers\nNational export agencies",
         visit="Exporters meeting European importers before committing to a stand\nCompanies researching certification and packaging requirements",
         url="https://www.fruitlogistica.com/en"),
    dict(name="BIOFACH", slug="biofach-nuremberg-2027", start=date(2027, 2, 16), end=date(2027, 2, 19),
         city="Nuremberg", venue="NürnbergMesse", organiser="NürnbergMesse",
         sectors="Organic food, Natural products, Ingredients",
         summary="The world's leading trade fair for organic food, with buyers from specialist retail, wholesale and processing.",
         description="The main event for certified organic food and ingredients. Buyers come from organic wholesale, specialist shops, supermarkets and food processors looking for reliable organic supply.",
         exhibit="Certified organic producers and exporters\nSuppliers of organic ingredients such as spices, oils, nuts and grains",
         visit="Producers preparing for organic certification and EU buyers\nExporters looking for organic importers",
         url="https://www.biofach.de/en"),
    dict(name="Anuga FoodTec", slug="anuga-foodtec-cologne-2027", start=date(2027, 2, 23), end=date(2027, 2, 26),
         city="Cologne", venue="Koelnmesse", organiser="Koelnmesse",
         sectors="Food processing, Packaging, Food technology",
         summary="International fair for food and beverage production technology, processing lines and packaging.",
         description="Focuses on the machines, packaging and digital systems used to produce food and drinks. Useful for processors abroad who are sourcing German equipment and for technology suppliers looking for international customers.",
         exhibit="Food machinery and packaging suppliers\nFood safety and automation providers",
         visit="Food processors planning to upgrade production lines\nCompanies sourcing German processing technology",
         url="https://www.anugafoodtec.com"),
    dict(name="ProWein", slug="prowein-duesseldorf-2027", start=date(2027, 3, 7), end=date(2027, 3, 9),
         city="Düsseldorf", venue="Messe Düsseldorf", organiser="Messe Düsseldorf",
         sectors="Wine, Spirits, Beverages",
         summary="Leading international trade fair for wines and spirits, for trade visitors only.",
         description="Brings wine and spirits producers together with importers, distributors, retailers and restaurant buyers. A key date for producers who want to enter the German and wider European drinks trade.",
         exhibit="Wine and spirits producers and cooperatives\nCraft and specialty beverage brands",
         visit="Producers meeting importers before deciding on a stand\nExporters researching label and price requirements",
         url="https://www.prowein-world.com"),
    dict(name="INTERNORGA", slug="internorga-hamburg-2027", start=date(2027, 3, 12), end=date(2027, 3, 16),
         city="Hamburg", venue="Hamburg Messe und Congress", organiser="Hamburg Messe und Congress",
         sectors="Hospitality, Foodservice, Bakery, Beverages, Kitchen equipment",
         summary="Annual fair for hotels, restaurants, catering and bakeries, from food and drinks to kitchen technology.",
         description="Serves the out-of-home market: hotels, restaurants, catering companies and bakeries. Buyers look for food and drink products, equipment and new concepts.",
         exhibit="Food and drink brands targeting hotels and restaurants\nFoodservice suppliers and equipment makers",
         visit="Producers looking for foodservice distributors\nCompanies researching the German hospitality market",
         url="https://www.internorga.com/en"),
    dict(name="ITB Berlin", slug="itb-berlin-2027", start=date(2027, 3, 16), end=date(2027, 3, 18),
         city="Berlin", venue="Messe Berlin", organiser="Messe Berlin",
         sectors="Tourism, Travel, Hospitality, Destinations",
         summary="The world's leading travel trade show, where destinations, tour operators and travel companies meet.",
         description="Destinations, tourism boards, hotels, tour operators and travel technology companies meet the international travel trade. A strong platform for tourism boards and operators who want German and European travellers.",
         exhibit="National and regional tourism boards\nTour operators, hotels and destination management companies",
         visit="Tourism businesses looking for German tour operators\nDestinations planning a future stand",
         url="https://www.itb.com/en"),
    dict(name="HANNOVER MESSE", slug="hannover-messe-2027", start=date(2027, 4, 5), end=date(2027, 4, 8),
         city="Hannover", venue="Hannover Exhibition Grounds", organiser="Deutsche Messe",
         sectors="Industry, Automation, Energy, Engineering, Digital",
         summary="The world's leading industrial technology fair, covering automation, energy, engineering and digital industry.",
         description="Shows the full range of industrial technology, from components and automation to energy systems and industrial software. Manufacturers and suppliers meet buyers, engineers and partners from around the world.",
         exhibit="Manufacturers and industrial suppliers\nEnergy and engineering companies",
         visit="Companies sourcing German industrial technology\nSuppliers looking for European partners and distributors",
         url="https://www.hannovermesse.de/en"),
    dict(name="Anuga", slug="anuga-cologne-2027", start=date(2027, 10, 9), end=date(2027, 10, 13),
         city="Cologne", venue="Koelnmesse", organiser="Koelnmesse",
         sectors="Food, Beverages, Retail, Private label",
         summary="One of the world's largest food and beverage fairs, held every two years, with buyers from retail and wholesale.",
         description="Covers almost every food and drink category, from dairy and meat to fine foods, drinks and organic products. Retail chains, wholesalers and importers from around the world come to find new suppliers.",
         exhibit="Food and beverage exporters across all categories\nNational pavilions and export agencies",
         visit="Exporters meeting European retail and wholesale buyers\nCompanies researching private-label opportunities",
         url="https://www.anuga.com"),
    dict(name="AGRITECHNICA", slug="agritechnica-hannover-2027", start=date(2027, 11, 14), end=date(2027, 11, 20),
         city="Hannover", venue="Hannover Exhibition Grounds", organiser="DLG",
         sectors="Agricultural machinery, AgriTech, Farm inputs",
         summary="The world's leading trade fair for agricultural machinery and equipment, held every two years.",
         description="The main event for tractors, harvesting equipment, crop protection, seed technology and digital farming. Dealers, farmers and agricultural companies from all over the world come to source equipment and partners.",
         exhibit="Agricultural machinery and component makers\nAgriTech and precision farming companies",
         visit="Dealers and distributors sourcing German farm machinery\nAgricultural companies looking for technology partners",
         url="https://www.agritechnica.com"),
]

REPRESENTED = [
    dict(name="ECOWAS Aviana West Africa International Expo", slug="ecowas-aviana-expo-2027",
         start=date(2027, 6, 22), end=date(2027, 6, 24), city="Ibadan", country="Nigeria",
         venue="University of Ibadan Conference Center", organiser="ECOWAS Aviana Expo",
         sectors="Poultry, Livestock, Animal feed, Veterinary, Agricultural machinery, AgriTech, Food processing",
         summary="Regional expo for poultry, livestock, feed and agricultural technology in West Africa.",
         description="Brings together suppliers of poultry, livestock, feed, veterinary products and agricultural technology with producers and buyers from West Africa. A route for German agricultural suppliers into the Nigerian and wider West African market.",
         exhibit="German suppliers of agricultural machinery and AgriTech\nAnimal health, feed and veterinary companies\nFood processing equipment suppliers",
         visit="", url="https://ecowasavianavivexpo.com/"),
    dict(name="Women Expo Ras Al Khaimah", slug="women-expo-ras-al-khaimah-2027",
         start=date(2027, 1, 19), end=date(2027, 1, 20), city="Ras Al Khaimah", country="United Arab Emirates",
         organiser="ZMZ Events", sectors="Beauty, Wellness, Fashion, Food, Lifestyle, Women-led business",
         summary="Business and consumer platform for beauty, wellness, fashion, lifestyle and women-led businesses in the UAE.",
         description="Connects brands in beauty, wellness, fashion, food and lifestyle with buyers and consumers in the UAE. Suited to German brands that want to test demand in the Gulf.",
         exhibit="German beauty, cosmetics and wellness brands\nFashion, jewellery and lifestyle companies\nWomen-led businesses entering the Gulf",
         visit="", url="https://www.zmzevents.com"),
    dict(name="Women Expo Al Khobar", slug="women-expo-al-khobar-2027",
         start=date(2027, 4, 14), end=date(2027, 4, 15), city="Al Khobar", country="Saudi Arabia",
         organiser="ZMZ Events", sectors="Beauty, Wellness, Fashion, Food, Lifestyle, Women-led business",
         summary="Business and consumer platform for beauty, wellness, fashion, lifestyle and women-led businesses in Saudi Arabia.",
         description="Connects brands in beauty, wellness, fashion, food and lifestyle with buyers and consumers in Saudi Arabia's Eastern Province. Suited to German brands that want a first step into the Saudi market.",
         exhibit="German beauty, cosmetics and wellness brands\nFashion, jewellery and lifestyle companies\nWomen-led businesses entering Saudi Arabia",
         visit="", url="https://www.zmzevents.com"),
    dict(name="Azerbaijan Mining Expo", slug="azerbaijan-mining-expo-2027",
         start=date(2027, 9, 8), end=date(2027, 9, 10), city="Baku", country="Azerbaijan",
         organiser="Azerbaijan Mining Expo", sectors="Mining, Metallurgy, Equipment, Engineering",
         summary="International exhibition for mining, metallurgy and related equipment in the Caspian region.",
         description="Brings mining and metallurgy companies together with equipment and service suppliers. A route for German mining technology and engineering firms into Azerbaijan and the Caspian region.",
         exhibit="German mining equipment and machinery makers\nEngineering, safety and environmental service providers",
         visit="", url="https://azerbaijanminingexpo.com"),
]


def seed(apps, schema_editor):
    TradeFair = apps.get_model("website", "TradeFair")
    for i, d in enumerate(GERMANY):
        TradeFair.objects.get_or_create(slug=d["slug"], defaults=dict(
            name=d["name"], kind="germany", start_date=d["start"], end_date=d["end"],
            city=d["city"], country="Germany", venue=d["venue"], organiser=d["organiser"],
            sectors=d["sectors"], summary=d["summary"], description=d["description"],
            who_should_exhibit=d["exhibit"], who_should_visit=d["visit"], how_we_help=HELP_GERMANY,
            official_url=d["url"], is_published=True, show_in_carousel=True, order=i,
        ))
    for i, d in enumerate(REPRESENTED):
        TradeFair.objects.get_or_create(slug=d["slug"], defaults=dict(
            name=d["name"], kind="represented", start_date=d["start"], end_date=d["end"],
            city=d["city"], country=d["country"], venue=d.get("venue", ""), organiser=d["organiser"],
            sectors=d["sectors"], summary=d["summary"], description=d["description"],
            who_should_exhibit=d["exhibit"], who_should_visit=d["visit"], how_we_help=HELP_REPRESENTED,
            our_role="Exhibitor recruitment partner for Germany", official_url=d["url"],
            is_published=False, show_in_carousel=True, order=i,
        ))


def unseed(apps, schema_editor):
    TradeFair = apps.get_model("website", "TradeFair")
    TradeFair.objects.filter(slug__in=[d["slug"] for d in GERMANY + REPRESENTED]).delete()


class Migration(migrations.Migration):
    dependencies = [("website", "0012_tradefair")]
    operations = [migrations.RunPython(seed, unseed)]
