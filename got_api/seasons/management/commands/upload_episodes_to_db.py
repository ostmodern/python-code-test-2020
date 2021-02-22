from django.core.management.base import BaseCommand
from seasons.services import upload_episodes_to_db


class Command(BaseCommand):
    def handle(self, *args, **options):
        upload_episodes_to_db()