from django.contrib import admin
from django.urls import path
from home.views import home, gold_volume_diario

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("home/gold/", gold_volume_diario, name="gold_volume_diario"),
]
