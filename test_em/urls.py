from django.contrib import admin
from django.urls import path

from auth_system.urls import urlpatterns as api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api)
]
