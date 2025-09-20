from django.urls import include, path
from . import views

urlpatterns = [
    # Political Party
    path(
        "create/",
        views.CreatePoliticalPartyAPI.as_view(),
        name="create-political-party",
    ),
    path(
        "get/list/",
        views.GetPoliticalPartyListAPI.as_view(),
        name="get-political-party-list",
    ),
    path(
        "get/detail/<int:pk>/",
        views.GetPoliticalPartyDetailAPI.as_view(),
        name="get-political-party-detail",
    ),
    path(
        "update/<int:pk>/",
        views.UpdatePoliticalPartyAPI.as_view(),
        name="update-political-party",
    ),
    path(
        "delete/<int:pk>/",
        views.DeletePoliticalPartyAPI.as_view(),
        name="delete-political-party",
    ),
]
