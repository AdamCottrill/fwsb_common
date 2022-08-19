"""uglmu_common URL Configuration
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("common/", include("common.urls", namespace="common")),
    path("api/v1/common/", include("common.api.urls", namespace="common_api")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
