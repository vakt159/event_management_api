from datetime import timedelta

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view, \
    OpenApiResponse, OpenApiParameter
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from event_management.filters import EventFilter
from event_management.models import Event, Registration
from event_management.permissions import IsOrganizerOrReadOnly
from event_management.serializers import EventSerializer, \
    EventRegistrationSerializer

from event_management.tasks import send_registration_email_task


@extend_schema_view(
    tags=["Events", ],
    list=extend_schema(
        summary="List events",
        description="Retrieve all events",
        responses=EventSerializer(many=True),
        parameters=[
            OpenApiParameter(
                name="date",
                type={"type": "string", "format": "date"},
                description="Filter events exactly at this date"
            ),
            OpenApiParameter(
                name="location",
                type=OpenApiTypes.STR,
                description="Filter by location"
            ),
            OpenApiParameter(
                name="title",
                type=OpenApiTypes.STR,
                description="Filter by title"
            ),
            OpenApiParameter(
                name="description",
                type=OpenApiTypes.STR,
                description="Filter by description"
            ),
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve event",
        description="Get single event by ID",
        responses=EventSerializer,
    ),
    create=extend_schema(
        summary="Create event",
        description="Create event. Organizer is set automatically to current user.",
        request=EventSerializer,
        responses={
            201: EventSerializer,
        },
    ),
    update=extend_schema(
        summary="Update event",
        description="Full update. Only organizer allowed.",
        request=EventSerializer,
        responses=EventSerializer,
    ),
    partial_update=extend_schema(
        summary="Partial update event",
        description="Partial update. Only organizer allowed.",
        request=EventSerializer,
        responses=EventSerializer,
    ),
    destroy=extend_schema(
        summary="Delete event",
        description="Delete event. Only organizer allowed.",
        responses={
            204: OpenApiResponse(description="Deleted"),
        },
    ),
)
class EventViewSet(ModelViewSet):
    queryset = Event.objects.all().order_by("id")
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated, IsOrganizerOrReadOnly)

    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter

    def get_serializer_class(self):
        if self.action == "register":
            return EventRegistrationSerializer
        return EventSerializer

    def perform_create(self, serializer):
        event = serializer.save(organizer=self.request.user)
        Registration.objects.create(
            user=self.request.user,
            event=event,
            status="registered"
        )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Register to event",
        description="Register current authenticated user to event",
        request=None,
        responses={
            200: OpenApiResponse(description="Registered successfully"),
            400: OpenApiResponse(description="Already registered"),
        },
    )
    @action(methods=["PATCH"], detail=True, permission_classes = [IsAuthenticated,], url_path="register")
    def register(self, request, pk=None):
        event = self.get_object()
        user = request.user

        registration, created = Registration.objects.get_or_create(
            user=user,
            event=event,
            defaults={"status": "registered"}
        )

        if not created:
            if registration.status == "registered":
                return Response(
                    {"detail": "Already registered"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            registration.status = "registered"
            registration.save()

        send_registration_email_task.delay(
            user.email, event.title, str(event.date), event.location
        )
        return Response(
            {"detail": "Registered successfully"},
            status=status.HTTP_200_OK
        )
