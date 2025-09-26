import json
import os
import secrets
import string
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.users.models import User
from apps.political_party.models import PoliticalParty
from utils.command_helpers.core import seed_data


class Command(BaseCommand):
    """
    Seeds the database with initial data from a JSON file.
    """

    help = "Seeds the database with initial data from a JSON file."

    def handle(self, *args, **options):
        seed_data()
