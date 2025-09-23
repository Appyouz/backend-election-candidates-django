from rest_framework import serializers

from apps.core.models import Address


class GetAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "uuid",
            "street_address",
            "street_address_2",
            "city",
            "region",
            "postal_code",
            "country",
            "latitude",
            "longitude",
        ]


class CreateAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "street_address",
            "street_address_2",
            "city",
            "region",
            "postal_code",
            "country",
            "latitude",
            "longitude",
        ]
        extra_kwargs = {
            "street_address": {"required": True, "allow_blank": False},
            "street_address_2": {"required": True, "allow_blank": True},
            "city": {"required": True, "allow_blank": False},
            "region": {"required": True, "allow_blank": True},
            "postal_code": {"required": True, "allow_blank": True},
            "country": {"required": True, "allow_blank": False},
            "latitude": {"required": True, "allow_null": True},
            "longitude": {"required": True, "allow_null": True},
        }


class UpdateAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "street_address",
            "street_address_2",
            "city",
            "region",
            "postal_code",
            "country",
            "latitude",
            "longitude",
        ]
