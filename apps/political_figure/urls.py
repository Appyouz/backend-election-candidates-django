from django.urls import include, path
from . import views

urlpatterns = [
    # Political Party
    path(
        "create/",
        views.CreatePoliticalFigureAPI.as_view(),
        name="create-political-party",
    ),
    path(
        "get/list/",
        views.GetPoliticalFigureListAPI.as_view(),
        name="get-political-party-list",
    ),
    path(
        "get/detail/<int:pk>/",
        views.GetPoliticalFigureDetailAPI.as_view(),
        name="get-political-party-detail",
    ),
    path(
        "update/<int:pk>/",
        views.UpdatePoliticalFigureAPI.as_view(),
        name="update-political-party",
    ),
    path(
        "delete/<int:pk>/",
        views.DeletePoliticalFigureAPI.as_view(),
        name="delete-political-party",
    ),
]
