from rest_framework import serializers
from apps.core.models import Address
from apps.core.serializers import CreateAddressSerializer, UpdateAddressSerializer
from apps.political_figure.models import PoliticalFigure


class CreatePoliticalFigureSerializer(serializers.ModelSerializer):

    home_address = CreateAddressSerializer()
    current_address = CreateAddressSerializer()

    class Meta:
        model = PoliticalFigure
        fields = [
            "full_name",
            "date_of_birth",
            "gender",
            "biography",
            "photo",
            "home_address",
            "current_address",
            "political_party",
            "contact_number",
            "website",
            "facebook_url",
            "twitter_url",
            "instagram_url",
            "is_active",
        ]

        extra_kwargs = {
            "full_name": {"required": True, "allow_blank": False},
            "date_of_birth": {"required": True, "allow_null": True},
            "gender": {"required": True, "allow_blank": False},
            "biography": {"required": True, "allow_blank": True},
            "photo": {
                "required": True,
                "allow_null": True,
            },
            "home_address": {"required": True, "allow_null": False},
            "current_address": {"required": True, "allow_null": False},
            # allow null for independent political figure
            "political_party": {
                "required": True,
                "allow_null": True,
                "error_messages": {"does_not_exist": "Political party does not exist"},
            },
            "contact_number": {"required": True, "allow_blank": True},
            "website": {"required": True, "allow_blank": True},
            "facebook_url": {"required": True, "allow_blank": True},
            "twitter_url": {"required": True, "allow_blank": True},
            "instagram_url": {"required": True, "allow_blank": True},
            "is_active": {"required": True, "allow_null": False},
        }


class UpdatePoliticalFigureSerializer(serializers.ModelSerializer):

    home_address = UpdateAddressSerializer()
    current_address = UpdateAddressSerializer()

    class Meta:
        model = PoliticalFigure
        fields = [
            "full_name",
            "date_of_birth",
            "gender",
            "biography",
            "photo",
            "home_address",
            "current_address",
            "political_party",
            "contact_number",
            "website",
            "facebook_url",
            "twitter_url",
            "instagram_url",
            "is_active",
        ]
