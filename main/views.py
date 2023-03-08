from django.db.models.expressions import Q
from main.models import User, Thesis, Message
from main.serializers import (
    TokenObtainPairSerializer,
    LoginSerializer,
    RegisterSerializer,
    TokenSerializer,
    UserSerializer,
    ThesisSerializer,
    MessageSerializer,
)
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins

# Create your views here.
class AuthViewSet(GenericViewSet):

    # Send verification code to user via email or phone
    @action(methods=["post"], detail=False)
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            user = User.objects.get(username=data["username"])

            if not user.check_password(data["password"]):
                raise PermissionDenied("نام کاربری و یا رمز عبور اشتباه است")

            token = TokenObtainPairSerializer(data=data)
            token.is_valid(raise_exception=True)
            return Response(TokenSerializer(token.validated_data).data)
        except (User.DoesNotExist):
            raise PermissionDenied("نام کاربری و یا رمز عبور اشتباه است")

    # Verify otp
    @action(methods=["post"], detail=False)
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            User.objects.get(
                Q(username=data["username"])
                | Q(phone_number=data["phone_number"])
                | Q(ssn=data["ssn"])
                | Q(national_code=data["national_code"])
            )
            raise PermissionDenied("کاربر با این مشخصات از قبل ثبت شده است")
        except User.DoesNotExist:
            user = User.objects.create(
                username=data["username"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                phone_number=data["phone_number"],
                email=data["email"],
            )
            user.set_password(data["password"])
            user.save(update_fields=["password"])

            token = TokenObtainPairSerializer(
                data={
                    "username": data["username"],
                    "password": data["password"],
                }
            )
            token.is_valid(raise_exception=True)
            return Response(TokenSerializer(token.validated_data).data)


class RefreeViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = User.objects.filter(role=User.teacher)
    serializer_class = UserSerializer


class ThesisViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
):
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch"]
    serializer_class = ThesisSerializer

    def get_queryset(self):
        return Thesis.objects.filter(
            Q(student=self.request.user) | Q(refree=self.request.user)
        )

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class MessageViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
):
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post"]
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(reciever=self.request.user)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
