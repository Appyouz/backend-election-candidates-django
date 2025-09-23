import json
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from django.db import transaction

from apps.users.models import User
from apps.political_party.models import PoliticalParty

class Command(BaseCommand):
    """
    Seeds the database with initial data from a JSON file.
    """
    help = 'Seeds the database with initial data from a JSON file.'

    @transaction.atomic
    def handle(self, *args, **options):
        # Define the JSON data file path
        file_path = os.path.join(settings.BASE_DIR, 'data', 'seed_data.json')

        self.stdout.write(f"Attempting to seed data from {file_path}...")

        try:
            # Read the JSON file
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            # Process Users
            users_data = data.get('users', [])
            for user_data in users_data:
                try:
                    # Create a user instance
                    user, created = User.objects.get_or_create(
                        username=user_data['username'],
                        defaults={
                            'email': user_data['email'],
                            'first_name': user_data.get('first_name', ''),
                            'last_name': user_data.get('last_name', ''),
                            'role': user_data.get('role', User.Roles.GENERAL),
                            'phone_number': user_data.get('phone_number', ''),
                        }
                    )
                    # Set password if the user was just created
                    if created:
                        user.set_password("password123")
                        user.save()
                        self.stdout.write(self.style.SUCCESS(
                            f"Successfully created user: {user.username}"
                        ))
                    else:
                        self.stdout.write(self.style.WARNING(
                            f"User already exists: {user.username}"
                        ))
                except (KeyError, ValidationError) as e:
                    self.stdout.write(self.style.ERROR(
                        f"Error processing user data: {user_data} - {e}"
                    ))

            # Process Political Parties
            parties_data = data.get('political_parties', [])
            for party_data in parties_data:
                try:
                    party, created = PoliticalParty.objects.get_or_create(
                        name=party_data['name'],
                        defaults={
                            'abbreviation': party_data['abbreviation'],
                            'founded_date': party_data['founded_date'],
                            'description': party_data.get('description', ''),
                            'website': party_data.get('website', ''),
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(
                            f"Successfully created political party: {party.name}"
                        ))
                    else:
                        self.stdout.write(self.style.WARNING(
                            f"Political party already exists: {party.name}"
                        ))
                except (KeyError, ValidationError) as e:
                    self.stdout.write(self.style.ERROR(
                        f"Error processing political party data: {party_data} - {e}"
                    ))

            self.stdout.write(self.style.SUCCESS('Database seeding complete!'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(
                f"Error: The file {file_path} was not found."
            ))
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(
                f"Error: The JSON file is malformed. Details: {e}"
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f"An unexpected error occurred: {e}"
            ))
