from django.shortcuts import get_object_or_404
from rest_framework import serializers
from apps.core.serializers import GetAddressSerializer
from ..models.core import PoliticalFigure
from utils.core.base_views import PublicAPIView
from utils.core.response_wrappers import NoContentResponse, OKResponse
from utils.political_figure.core import PoliticalFigureUtil
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from drf_spectacular.utils import extend_schema


class GetPoliticalFigureDetailAPI(PublicAPIView):
    """
    Get political figure detail
    """

    class OutputSerializer(serializers.ModelSerializer):
        political_party_name = serializers.CharField(source="political_party.name")
        political_party_slug = serializers.CharField(source="political_party.slug")

        home_address = GetAddressSerializer()
        current_address = GetAddressSerializer()

        class Meta:
            model = PoliticalFigure
            fields = [
                "id",
                "uuid",
                "slug",
                "full_name",
                "date_of_birth",
                "gender",
                "biography",
                "photo",
                "home_address",
                "current_address",
                "political_party_name",
                "political_party_slug",
                "contact_number",
                "website",
                "facebook_url",
                "twitter_url",
                "instagram_url",
                "is_active",
            ]
            # required by drf spectacular if we need to use same name (OutputSerializer) for different serializers
            ref_name = "PoliticalFigureDetailSerializer"

    output_serializer = OutputSerializer

    @extend_schema(responses=output_serializer)
    def get(self, request, pk):
        # prefetch addresses
        qs = PoliticalFigure.objects.all().prefetch_related(
            "home_address", "current_address"
        )
        political_figure = get_object_or_404(qs, pk=pk)
        serializer = self.output_serializer(instance=political_figure)
        return OKResponse(data=serializer.data)


class GetPoliticalFigureListAPI(PublicAPIView):
    """
    Get political figure list
    """

    output_serializer = GetPoliticalFigureDetailAPI.OutputSerializer

    @extend_schema(responses=output_serializer(many=True))
    def get(self, request):
        political_figures = PoliticalFigure.objects.all().prefetch_related(
            "home_address", "current_address"
        )
        serializer = self.output_serializer(instance=political_figures, many=True)
        return OKResponse(data=serializer.data)


class CreatePoliticalFigureAPI(PublicAPIView):
    """
    Create political figure.
    For creating via drf-spectacular form, send `null` wherever a file is expected, and empty string wherever a string `""` is expected and value is optional
    """

    # NOTE: we need the multipart parser and form parser for file upload
    # But also allow JSONParser so that user can create using drf-spectacular's swagger ui.
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    output_serializer = GetPoliticalFigureDetailAPI.OutputSerializer

    @extend_schema(
        request=PoliticalFigureUtil.create_serializer, responses=output_serializer
    )
    def post(self, request):
        data = request.data

        print(data, "data")
        political_figure = PoliticalFigureUtil.create_political_figure(data)

        # prepare output
        output_data = self.output_serializer(political_figure).data

        return OKResponse(data=output_data)


class UpdatePoliticalFigureAPI(PublicAPIView):
    """
    Update political figure.
    For updating via drf-spectacular form, send `null` wherever a file is expected, and empty string wherever a string `""` is expected and value is optional.
    Don't send the fields that you don't want to update cause this is a patch update.
    """

    # NOTE: we need the multipart parser and form parser for file upload
    # But also allow JSONParser so that user can create using drf-spectacular's swagger ui.
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    output_serializer = GetPoliticalFigureDetailAPI.OutputSerializer

    @extend_schema(
        request=PoliticalFigureUtil.update_serializer, responses=output_serializer
    )
    def patch(self, request, pk):
        political_figure = get_object_or_404(PoliticalFigure, pk=pk)

        data = request.data

        PoliticalFigureUtil.update_political_figure(political_figure, data)

        # photo field becomes null somehow only on the returned object from PoliticalFigureUtil.update_political_figure (but is set correctly in the database), so instead just fetch again to provide correct output

        updated_political_figure = (
            PoliticalFigure.objects.all()
            .prefetch_related("home_address", "current_address")
            .get(pk=political_figure.pk)
        )

        # prepare output data
        serializer = self.output_serializer(instance=updated_political_figure)
        return OKResponse(data=serializer.data)


class DeletePoliticalFigureAPI(PublicAPIView):
    """
    Delete political figure
    """

    @extend_schema(responses=None)
    def delete(self, request, pk):
        political_figure = get_object_or_404(PoliticalFigure, pk=pk)
        PoliticalFigureUtil.delete_political_figure(political_figure=political_figure)
        return NoContentResponse()
