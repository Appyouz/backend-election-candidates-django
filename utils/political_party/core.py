from apps.political_party.models import PoliticalParty
from apps.political_party.serializers import (
    CreatePoliticalPartySerializer,
    UpdatePoliticalPartySerializer,
)


class PoliticalPartyUtil:
    """
    Single Source of truth for data mutation and some fetch operation for political party
    """

    create_serializer = CreatePoliticalPartySerializer
    update_serializer = UpdatePoliticalPartySerializer

    @staticmethod
    def create_political_party(data):
        """
        NOTE: Uses pattern used in https://github.com/HackSoftware/Django-Styleguide
        Creates and returns political party.
        """
        serializer = PoliticalPartyUtil.create_serializer(data=data)

        # serializer's ValidationError is automatically handled in exception handler
        serializer.is_valid(raise_exception=True)

        political_party = serializer.save()

        return political_party

    @staticmethod
    def update_political_party(political_party: PoliticalParty, data):
        """
        Updates and returns political party.
        """
        serializer = PoliticalPartyUtil.update_serializer(
            instance=political_party, data=data, partial=True
        )

        # serializer's ValidationError is automatically handled in exception handler
        serializer.is_valid(raise_exception=True)

        political_party = serializer.save()

        return political_party

    @staticmethod
    def delete_political_party(political_party: PoliticalParty):
        political_party.delete()
