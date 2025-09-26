"""
URL configuration for electionsys project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from django.conf import settings
from utils.core.constants import API_V1_PREFIX
from django.conf.urls.static import static

urlpatterns = [
    # NOTE: We'll have our own dashboard in NextJS, so don't use django admin
    # path('admin/', admin.site.urls),
    path(f"{API_V1_PREFIX}/political-parties/", include("apps.political_party.urls")),
    path(f"{API_V1_PREFIX}/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(f"{API_V1_PREFIX}/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path(f"{API_V1_PREFIX}/docs/redoc", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path(f"{API_V1_PREFIX}/core/", include("apps.core.urls")),
    path(f"{API_V1_PREFIX}/political-figures/", include("apps.political_figure.urls")),
    path(f"{API_V1_PREFIX}/users/", include("apps.users.urls")),
]

if settings.DEBUG:
    # In production, debug is False, and the below files will be served by nginx
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
