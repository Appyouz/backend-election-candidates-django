from django.conf import settings
from django.core.management.base import BaseCommand
from utils.command_helpers.core import seed_data


class Command(BaseCommand):
    """
    Sets up the server.
    - Seeds data
    """

    help = """
            Sets up the server.
            - Seeds data
            """

    def handle(self, *args, **options):
        seed_data()
