from django.db import migrations

# Snapshot of the packages and founder profile at the time of this migration.
# Kept here (not imported from content.py) so the migration never changes later.
PACKAGES = {
    "trade-fair-representation-germany": [
        ("Fair day", "From €650", "per fair day + ticket and travel at cost", "One fair, one clear goal", False,
         "Pre-fair briefing call\nAttendance or booth support for one day\nLead list with notes\nPhotos and a short written report"),
        ("Fair + follow-up", "From €950", "per fair day + ticket and travel at cost", "Turning fair contacts into meetings", True,
         "Everything in Fair day\nFollow-up of every lead for 3 weeks\nBooking of first calls or meetings\nFinal summary with next steps"),
        ("Multi-day or booth staffing", "By quote", "", "Several days, several fairs or a full booth", False,
         "Scope agreed on a call\nDaily reporting during the fair\nFollow-up included"),
    ],
    "find-business-partners-germany": [
        ("Partner shortlist", "€490", "one-off", "Seeing who is out there before you invest more", False,
         "30 checked potential partners\nWhy each one fits, plus contact routes\nShort market notes"),
        ("Shortlist + outreach", "From €890", "+ €1,200 per signed partner", "Getting real conversations started", True,
         "Everything in Partner shortlist\nPersonal outreach to the best 15\nReply tracking and follow-up\nFirst introduction calls set up"),
        ("Custom search", "By quote", "", "Several sectors, countries or partner types", False,
         "Scope agreed on a call\nRegular progress updates"),
    ],
    "germany-market-entry-support": [
        ("Entry check", "€390", "one-off", "A fast, honest first view", False,
         "60-minute call\nWritten one-page entry route\nPrice and positioning notes\nRecommended first fair or partner route"),
        ("Entry plan + first contacts", "From €990", "one-off", "Starting with real contacts", True,
         "Everything in Entry check\nMarket and competitor snapshot\nShortlist of 20 first contacts\nPersonal outreach to the best 10"),
        ("Ongoing support", "From €290", "per month, after a first project", "Keeping momentum after the first results", False,
         "Monthly priorities and follow-up\nMonthly progress report"),
    ],
    "eu-local-representative-germany": [
        ("Local contact", "From €290", "per month, minimum 3 months", "Being reachable in Germany", False,
         "Named contact person in Germany\nAnswers to partner enquiries in German and English\nMonthly update"),
        ("Local contact + meetings", "From €490", "per month, minimum 3 months", "Active relationship building", True,
         "Everything in Local contact\nUp to 2 meetings a month\nFollow-up management"),
    ],
    "distributor-search-germany": [
        ("Distributor shortlist", "€490", "one-off", "Knowing which distributors fit", False,
         "25 checked distributor candidates\nWhy each one fits, plus contact routes\nNotes on what they usually expect"),
        ("Shortlist + outreach", "From €890", "+ €1,200 per signed distributor", "Getting distributor talks started", True,
         "Everything in Distributor shortlist\nPersonal outreach to the best 12\nSample and price-list follow-up\nFirst talks set up"),
        ("Custom search", "By quote", "", "Several product lines or EU countries", False,
         "Scope agreed on a call\nRegular progress updates"),
    ],
    "trade-fair-follow-up-lead-management": [
        ("Follow-up sprint", "€350", "up to 50 leads, 4 weeks", "Not losing contacts after a fair", False,
         "Lead list cleaned and ranked\nPersonal follow-up of every lead\nReply tracking\nSummary of who is interested"),
        ("Follow-up + meetings", "From €590", "up to 100 leads, 4 weeks", "Turning interest into calls", True,
         "Everything in Follow-up sprint\nCalls or meetings booked\nNext-step notes for each hot lead"),
    ],
}

FOUNDER = dict(
    name="Ivan Nkomati",
    role="Founder & Managing Partner",
    location="Leipzig, Germany",
    photo_url="/static/website/img/ivan-nkomati.webp",
    linkedin_url="https://www.linkedin.com/in/ivan-nkomati-313637228",
    intro="TradeGate is run from Leipzig, in German and English. You get one named contact, from the first call to the final report.",
    partners_text="Behind every project stands a network of independent specialists we work with, such as trade-fair staff, translators, sector consultants and legal and tax advisers in Germany. We bring in the right people for each project's scope, and you keep one contact throughout.",
)


def seed(apps, schema_editor):
    ServicePackage = apps.get_model("website", "ServicePackage")
    TeamProfile = apps.get_model("website", "TeamProfile")
    if not ServicePackage.objects.exists():
        for slug, rows in PACKAGES.items():
            for i, (name, price, unit, best_for, featured, includes) in enumerate(rows):
                ServicePackage.objects.create(service_slug=slug, name=name, price=price, unit=unit,
                                              best_for=best_for, featured=featured, includes=includes, order=i)
    if not TeamProfile.objects.exists():
        TeamProfile.objects.create(**FOUNDER)


def unseed(apps, schema_editor):
    apps.get_model("website", "ServicePackage").objects.all().delete()
    apps.get_model("website", "TeamProfile").objects.filter(name=FOUNDER["name"]).delete()


class Migration(migrations.Migration):
    dependencies = [("website", "0014_partner_materials_packages_team")]
    operations = [migrations.RunPython(seed, unseed)]
