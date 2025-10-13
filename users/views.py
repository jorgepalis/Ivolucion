from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import User
from .serializers import UserDetailSerializer
from rest_framework.permissions import IsAuthenticated

from .serializers import RegisterSerializer, RegisterResponseSerializer

@extend_schema(tags=["Users"])
class RegisterView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        request=RegisterSerializer,
        responses={201: RegisterResponseSerializer},
        auth=None,
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Users"])
class CustomTokenObtainPairView(TokenObtainPairView):
    pass

@extend_schema(tags=["Users"])
class CustomTokenRefreshView(TokenRefreshView):
    pass


@extend_schema(tags=["Users"])
class MeView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        request=None,
        responses={200: UserDetailSerializer},
        auth=None,
    )
    def get(self, request):
        user = request.user
        serializer = UserDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
