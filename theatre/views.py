from datetime import datetime
from rest_framework.decorators import action
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from rest_framework.pagination import PageNumberPagination
from theatre.models import (Genre, Actor, TheatreHall,
                            Play, Performance, Reservation)
from theatre.permission import IsAdminOrIfAuthenticatedReadOnly
from theatre.serializers import (GenreSerializer,
                                 ActorSerializer,
                                 TheatreHallSerializer,
                                 PlaySerializer,
                                 PlayListSerializer,
                                 PlayDetailSerializer,
                                 PerformanceSerializer,
                                 PerformanceListSerializer,
                                 PerformanceDetailSerializer,
                                 ReservationSerializer,
                                 TheatreHallDetailSerializer,
                                 ActorDetailSerializer,
                                 ReservationListSerializer,
                                 PlayImageSerializer)


class GenreViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class ActorViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):

        if self.action == "retrieve":
            return ActorDetailSerializer
        return ActorSerializer


class TheatreHallViewSet(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):

        if self.action == "retrieve":
            return TheatreHallDetailSerializer
        return TheatreHallSerializer


class PlayViewSet(ReadOnlyModelViewSet,
                  mixins.CreateModelMixin,
                  GenericViewSet):
    queryset = Play.objects.all()
    serializer_class = PlaySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return PlayListSerializer

        if self.action == "retrieve":
            return PlayDetailSerializer

        if self.action == "upload_image":
            return PlayImageSerializer

        return PlaySerializer

    @staticmethod
    def _params_to_ints(qs):
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):

        title = self.request.query_params.get("title")
        genres = self.request.query_params.get("genres")
        actors = self.request.query_params.get("actors")

        queryset = self.queryset

        if title:
            queryset = queryset.filter(title__icontains=title)

        if genres:
            genres_ids = self._params_to_ints(genres)
            queryset = queryset.filter(genres__id__in=genres_ids)

        if actors:
            actors_ids = self._params_to_ints(actors)
            queryset = queryset.filter(actors__id__in=actors_ids)

        return queryset.distinct()

    @action(
        methods=["POST"],
        detail=True,
        permission_classes=[IsAdminUser],
        url_path="upload-image",
    )
    def upload_image(self, request, pk=None):
        play = self.get_object()
        serializer = self.get_serializer(play, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class PerformanceViewSet(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return PerformanceListSerializer

        if self.action == "retrieve":
            return PerformanceDetailSerializer

        return PerformanceSerializer

    def get_queryset(self):
        date = self.request.query_params.get("date")
        play_id_str = self.request.query_params.get("play")

        queryset = self.queryset

        if date:
            date = datetime.strptime(date, "%Y-%m-%d").date()
            queryset = queryset.filter(show_time__date=date)

        if play_id_str:
            queryset = queryset.filter(play_id=int(play_id_str))

        return queryset.distinct()


class OrderPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class ReservationViewSet(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         GenericViewSet,):
    queryset = Reservation.objects
    serializer_class = ReservationSerializer
    pagination_class = OrderPagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        if self.action == "list":
            queryset = queryset.prefetch_related(
                "tickets__performance__theatre_hall")
        return queryset.order_by('created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        serializer = self.serializer_class
        if self.action == "list":
            return ReservationListSerializer
        return serializer
