from django.urls import include, path
from . import views

urlpatterns = [
    # Political Party
    path(
        "countries/get/list/",
        views.GetCountryListAPI.as_view(),
        name="get-country-list",
    ),
]
