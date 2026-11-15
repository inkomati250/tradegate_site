from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Delete visitor statistics older than about 13 months (privacy policy, section 11)."

    def handle(self, *args, **options):
        from website.analytics import prune
        self.stdout.write(f"Old visitor statistics deleted: {prune()}")
