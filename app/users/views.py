from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_200_OK


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def login_view(request):
    username = request.data.get("username", None)
    password = request.data.get("password", None)

    if settings.SERVICE_USER == username and settings.SERVICE_PASSWORD == password:
        user, _ = User.objects.get_or_create(
            username=username, first_name="Anonymous", last_name="User"
        )
        login(request, user)
        return Response(status=HTTP_200_OK)
    else:
        return Response(
            {"message": "Invalid login or password!"}, status=HTTP_403_FORBIDDEN
        )


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({"message": "You are logged out!"}, status=HTTP_200_OK)


class CustomAuthToken(ObtainAuthToken):
    """Custom obtain token class"""

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            token, created = Token.objects.get_or_create(user=request.user.pk)
            return Response({"token": token.key})
        else:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_403_FORBIDDEN,
            )
