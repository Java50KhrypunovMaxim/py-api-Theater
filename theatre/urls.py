from django.urls import path, include
from rest_framework import routers
from theatre.views import (GenreViewSet, ActorViewSet,
                           TheatreHallViewSet, PlayViewSet,
                           PerformanceViewSet, ReservationViewSet)

router = routers.DefaultRouter()
router.register("genres", GenreViewSet)
router.register("actors", ActorViewSet)
router.register("theatre_halls",
                TheatreHallViewSet)
router.register("plays", PlayViewSet)
router.register("performances", PerformanceViewSet)
router.register("reservation", ReservationViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "theatre"
