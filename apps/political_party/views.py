from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from apps.political_party.models import PoliticalParty
from utils.core.base_views import PublicAPIView
from utils.core.response_wrappers import OKResponse, NoContentResponse
from utils.political_party.core import PoliticalPartyUtil


# ---------- DETAIL ----------

class GetPoliticalPartyDetailAPI(PublicAPIView):
    extra_permissions = []

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = PoliticalParty
            fields = [
                "id",
                "name",
                "description",
                "slug",
                "abbreviation",
                "founded_date",
                "ideology",
                "hq_location",
                "website",
                "logo_url",
            ]

    output_serializer = OutputSerializer

    @extend_schema(responses=OutputSerializer)
    def get(self, request, pk):
        party = get_object_or_404(PoliticalParty, pk=pk)
        serializer = self.output_serializer(instance=party)
        return OKResponse(data=serializer.data)


# ---------- LIST ----------
@extend_schema(
    responses=PoliticalPartyUtil.create_serializer
)
class GetPoliticalPartyListAPI(PublicAPIView):
    extra_permissions = []

    output_serializer = GetPoliticalPartyDetailAPI.OutputSerializer

    def get(self, request):
        parties = PoliticalParty.objects.all().order_by("-created_at")
        serializer = self.output_serializer(parties, many=True)
        return OKResponse(data=serializer.data)


# ---------- CREATE ----------
@extend_schema(
    request=PoliticalPartyUtil.create_serializer,
    responses=PoliticalPartyUtil.create_serializer
)
class CreatePoliticalPartyAPI(PublicAPIView):
    extra_permissions = []

    output_serializer = GetPoliticalPartyDetailAPI.OutputSerializer

    def post(self, request):
        data = request.data
        political_party = PoliticalPartyUtil.create_political_party(data)

        # prepare output data
        output_data = self.output_serializer(political_party).data

        return OKResponse(
            data=output_data, message="Political Party created successfully"
        )


# ---------- UPDATE ----------
@extend_schema(
    request=PoliticalPartyUtil.create_serializer,
    responses=GetPoliticalPartyDetailAPI.OutputSerializer
)
class UpdatePoliticalPartyAPI(PublicAPIView):
    extra_permissions = []

    output_serializer = GetPoliticalPartyDetailAPI.OutputSerializer

    def patch(self, request, pk):
        political_party = get_object_or_404(PoliticalParty, pk=pk)

        data = request.data

        updated_political_party = PoliticalPartyUtil.update_political_party(
            political_party, data
        )

        # prepare output data
        party = self.output_serializer(updated_political_party).data

        return OKResponse(data=party, message="Political Party updated successfully")


# ---------- DELETE ----------
@extend_schema(responses=None)
class DeletePoliticalPartyAPI(PublicAPIView):
    extra_permissions = []

    def delete(self, request, pk):
        political_party = get_object_or_404(PoliticalParty, pk=pk)

        PoliticalPartyUtil.delete_political_party(political_party)

        return NoContentResponse(message="Political Party deleted successfully")
