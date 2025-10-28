from rest_framework import serializers
from apps.core.models import Address
from apps.core.serializers import CreateAddressSerializer, UpdateAddressSerializer
from .models.core import PoliticalFigure
from .models.achievements import Achievement

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



class AchievementSerializer(serializers.ModelSerializer):
    """
    Serializer for the Achievement model. Handles input validation and output formatting.
    """
    # Read-only field for displaying the figure's full name
    political_figure_full_name = serializers.CharField(
        source='political_figure.full_name', 
        read_only=True
    )
    
    class Meta:
        model = Achievement
        fields = [
            'id', 
            'uuid', 
            'political_figure', 
            'political_figure_full_name',
            'title', 
            'category', 
            'description', 
            'year', 
            'awarding_body', 
            'evidence_link', 
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'uuid', 'political_figure_full_name', 'created_at', 'updated_at'] 
        
    def validate_year(self, value):
        """
        Serializer-level validation to prevent future dates.
        The model validator handles the 4-digit format.
        """
        import datetime
        if value > datetime.date.today().year:
            raise serializers.ValidationError("Achievement year cannot be in the future.")
        return value
