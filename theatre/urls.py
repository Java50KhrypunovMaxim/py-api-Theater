from django.urls import path, include
from rest_framework import routers

from theatre.models import Performance
from theatre.views import GenreViewSet, ActorViewSet, TheatreHallViewSet, PlayViewSet, PerformanceViewSet

router = routers.DefaultRouter()
router.register("genres", GenreViewSet)
router.register("actors", ActorViewSet)
router.register("theatre_halls", TheatreHallViewSet)
router.register("plays", PlayViewSet)
router.register("performances", PerformanceViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "theatre"