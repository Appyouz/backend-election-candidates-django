from django.shortcuts import get_object_or_404
from rest_framework import serializers
from apps.core.serializers import GetAddressSerializer
from apps.political_figure.models import PoliticalFigure
from utils.core.base_views import PublicAPIView
from utils.core.response_wrappers import NoContentResponse, OKResponse
from utils.political_figure.core import PoliticalFigureUtil
from rest_framework.parsers import MultiPartParser, FormParser


class GetPoliticalFigureDetailAPI(PublicAPIView):
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

    output_serializer = OutputSerializer

    def get(self, request, pk):
        # prefetch addresses
        qs = PoliticalFigure.objects.all().prefetch_related(
            "home_address", "current_address"
        )
        political_figure = get_object_or_404(qs, pk=pk)
        serializer = self.output_serializer(instance=political_figure)
        return OKResponse(data=serializer.data)


class GetPoliticalFigureListAPI(PublicAPIView):
    output_serializer = GetPoliticalFigureDetailAPI.OutputSerializer

    def get(self, request):
        political_figures = PoliticalFigure.objects.all().prefetch_related(
            "home_address", "current_address"
        )
        serializer = self.output_serializer(instance=political_figures, many=True)
        return OKResponse(data=serializer.data)


class CreatePoliticalFigureAPI(PublicAPIView):

    # NOTE: we need the multipart parser and form parser for file upload
    parser_classes = [MultiPartParser, FormParser]

    output_serializer = GetPoliticalFigureDetailAPI.OutputSerializer

    def post(self, request):
        data = request.data
        political_figure = PoliticalFigureUtil.create_political_figure(data)

        # prepare output
        output_data = self.output_serializer(political_figure).data

        return OKResponse(data=output_data)


class UpdatePoliticalFigureAPI(PublicAPIView):

    parser_classes = [MultiPartParser, FormParser]

    output_serializer = GetPoliticalFigureDetailAPI.OutputSerializer

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
    def delete(self, request, pk):
        political_figure = get_object_or_404(PoliticalFigure, pk=pk)
        PoliticalFigureUtil.delete_political_figure(political_figure=political_figure)
        return NoContentResponse()
