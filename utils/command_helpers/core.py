import json
import os
import secrets
import string
import traceback
from typing import Dict, List
from django.conf import settings
from django.contrib.auth import get_user_model
from apps.political_figure.models import PoliticalFigure
from apps.political_party.models import PoliticalParty
from django.core.exceptions import ValidationError
from django.db import transaction

from utils.political_figure.core import PoliticalFigureUtil
from utils.political_party.core import PoliticalPartyUtil

User = get_user_model()


# ANSI escape code for green (success) text
RESET = "\033[39m"  # Reset the color to default
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RED = "\033[31m"


def print_success(message, *args, **kwargs):
    print(f"{GREEN}{message}{RESET}", *args, **kwargs)


def print_error(message, *args, **kwargs):
    print(f"{RED}{message}{RESET}", *args, **kwargs)


def print_warning(message, *args, **kwargs):
    print(f"{YELLOW}{message}{RESET}", *args, **kwargs)


def print_info(message, *args, **kwargs):
    print(f"{BLUE}{message}{RESET}", *args, **kwargs)


@transaction.atomic
def seed_data():
    # Define the path to JSON data file
    file_path = os.path.join(settings.BASE_DIR, "data", "seed_data.json")
    print_info(f"Attempting to seed data from {file_path}...")

    try:
        # Read the JSON file
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Process Users
        users_data = data.get("users", [])

        seed_users(users_data)

        # Process Political Parties
        parties_data = data.get("political_parties", [])

        seed_political_parties(parties_data)

        print_success("Database seeding complete!")

    except FileNotFoundError:
        print_error(f"Error: The file {file_path} was not found.")
    except json.JSONDecodeError as e:
        print_error(f"Error: The JSON file is malformed. Details: {e}")
    except Exception as e:
        print_error(f"An unexpected error occurred: {e}")
        traceback.print_exc()


def _generate_password():
    """Generates a secure, random password."""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return "".join(secrets.choice(alphabet) for _ in range(12))


def seed_users(users_data: List[Dict[str, str]]):
    for user_data in users_data:
        try:
            # Create a user instance
            user, created = User.objects.get_or_create(
                username=user_data["username"],
                defaults={
                    "email": user_data["email"],
                    "first_name": user_data.get("first_name", ""),
                    "last_name": user_data.get("last_name", ""),
                    "role": user_data.get("role", User.Roles.GENERAL),
                    "phone_number": user_data.get("phone_number", ""),
                },
            )
            # Set password if the user was just created
            if created:
                # Use a randomly generated password
                generated_password = _generate_password()
                user.set_password(generated_password)
                user.save()
                print_success(f"Successfully created user: {user.username}")
                print_warning(
                    f"Generated password for '{user.username}': {generated_password}"
                )
            else:
                print_warning(f"User already exists: {user.username}")
        except (KeyError, ValidationError) as e:
            print_error(f"Error processing user data: {user_data} - {e}")


def seed_political_parties(parties_data: List[Dict[str, str | List[Dict[str, str]]]]):
    print_info("Processing political parties...")
    for party_data in parties_data:
        try:

            political_figures_data = party_data.pop("political_figures", None)

            political_party = PoliticalParty.objects.filter(
                name=party_data["name"],
                abbreviation=party_data["abbreviation"],
                founded_date=party_data["founded_date"],
            ).first()

            if not political_party:
                # Political party does not exist, create it
                political_party = PoliticalPartyUtil.create_political_party(party_data)
                print_success(
                    f"Successfully created political party: {political_party.name}"
                )

            else:
                print_warning(f"Political party already exists: {political_party.name}")

            if political_figures_data:
                for political_figure_data in political_figures_data:
                    political_figure_data["political_party"] = political_party.pk

                    political_figure = PoliticalFigure.objects.filter(
                        full_name=political_figure_data["full_name"],
                        date_of_birth=political_figure_data["date_of_birth"],
                        gender=political_figure_data["gender"],
                        political_party=political_party,
                    ).first()

                    if not political_figure:
                        PoliticalFigureUtil.create_political_figure(
                            political_figure_data
                        )
                        print_success(
                            f"Successfully created political figure: {political_figure_data['full_name']}"
                        )
                    else:
                        print_warning(
                            f"Political figure already exists: {political_figure_data['full_name']}"
                        )
            else:
                print_warning(
                    f"No political figure data provided for political party: {political_party.name}"
                )

        except (KeyError, ValidationError) as e:
            print_error(f"Error processing political party data: {party_data} - {e}")
