from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import generics

from user.serializers import UserSerializer


@extend_schema(
    summary="User registration",
    description=(
        "Creates a new user account.\n\n"
    ),
    request=UserSerializer,
    responses={
        201: UserSerializer,
        400: OpenApiResponse(description="Validation error"),
    },
)
class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer