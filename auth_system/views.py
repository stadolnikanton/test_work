from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from .models import User

register_response = openapi.Response(
    description="Успешная регистрация",
    examples={
        "application/json": {
            "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
            "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        }
    },
)


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Регистрация нового пользователя",
        request_body=RegisterSerializer,
        responses={201: register_response, 400: "Ошибка валидации данных"},
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            refresh.payload.update(
                {
                    "user_id": user.id,
                    "firstname": user.first_name,
                    "lastname": user.last_name,
                }
            )

            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Вход в систему",
        request_body=LoginSerializer,
        responses={200: register_response, 400: "Неверный email или пароль"},
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]

            refresh = RefreshToken.for_user(user)
            refresh.payload.update(
                {
                    "user_id": user.id,
                    "firstname": user.first_name,
                    "lastname": user.last_name,
                }
            )

            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            )

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Выход из системы",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "refresh": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Refresh токен"
                )
            },
            required=["refresh"],
        ),
        responses={200: "Успешный выход", 400: "Неверный токен"},
    )
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Успешный выход"})
        except Exception:
            return Response({"error": "Неверный токен"}, status=HTTP_400_BAD_REQUEST)


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Получение данных профиля", responses={200: UserSerializer}
    )
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Обновление данных профиля",
        request_body=UserSerializer,
        responses={200: UserSerializer, 400: "Ошибка валидации"},
    )
    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class DeleteAccountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Удаление аккаунта (мягкое)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "refresh": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Refresh токен (опционально)"
                )
            },
        ),
        responses={200: "Аккаунт деактивирован и выполнен выход"},
    )
    def post(self, request):
        user = request.user
        user.is_active = False
        user.save()

        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
        except Exception:
            pass

        return Response({"message": "Аккаунт деактивирован и выполнен выход"})
