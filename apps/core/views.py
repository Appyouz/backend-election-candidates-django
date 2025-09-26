from django.shortcuts import render
from django_countries import countries

from utils.core.base_views import PublicAPIView
from rest_framework import serializers

from utils.core.general import get_country_list
from utils.core.response_wrappers import OKResponse
from drf_spectacular.utils import extend_schema


class GetCountryListAPI(PublicAPIView):

    class OutputSerializer(serializers.Serializer):
        code = serializers.CharField()
        name = serializers.CharField()

    output_serializer = OutputSerializer

    @extend_schema(responses=output_serializer(many=True))
    def get(self, request):
        data = get_country_list()

        serializer = self.output_serializer(instance=data, many=True)
        return OKResponse(data=serializer.data)
