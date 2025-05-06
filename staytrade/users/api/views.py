from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate

from staytrade.users.models import User
from .serializers import UserSerializer


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def token(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        print(username)
        if not username or not password:
            return Response(
                {"error": _("Both username and password are required")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {"error": _("Invalid credentials")}, status=status.HTTP_401_UNAUTHORIZED
            )

        # Get or create a token for the user
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
                "email": user.email,
                "is_new_token": created,
            }
        )

    @action(detail=False, methods=["post"])
    def logout(self, request):
        try:
            request.user.auth_token.delete()
            return Response(
                {"success": _("Successfully logged out")}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
