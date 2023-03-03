import math
import random
from utils.redis import redis
from django.db.models.expressions import Q
from main.models import User, Thesis, Message
from main.serializers import (
    SendVerificationCodeSerializer,
    TokenObtainPairSerializer,
    VerifyCodeResponseSerializer,
    VerifyCodeSerializer,
    UserSerializer,
    ThesisSerializer,
    MessageSerializer,
)
from rest_framework.decorators import action
from rest_framework.exceptions import (
    NotAcceptable,
    NotFound,
    Throttled,
    PermissionDenied,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins

# Create your views here.
class AuthViewSet(GenericViewSet):

    # Send verification code to user via email or phone
    @action(methods=["post"], detail=False)
    def send_verification_code(self, request):
        serializer = SendVerificationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data.get("phone_number", None)

        data = {}
        data["phone_number"] = phone_number

        # Get user if exists in database otherwise create a new user
        try:
            user = User.objects.get(**data)
        except User.DoesNotExist:
            data["username"] = phone_number
            user = User.objects.create(**data)

        if not user.is_active:
            raise PermissionDenied(detail="حساب کاربری شما غیر فعال شده است")

        # Checking otp expire time
        if redis.get(f"user_{user.id}_otp"):
            pttl = redis.pttl(f"user_{user.id}_otp")
            remaining_time = math.ceil(pttl / 1000)
            raise Throttled(detail=f"بعد از {remaining_time} ثانیه مجدداً تلاش کنید")

        # Generate otp
        code = str(random.randint(100000, 999999))
        try:
            print(code)
            redis.set(f"user_{user.id}_otp", code, ex=120)
            response = {"detail": "کد با موفقیت ارسال شد", "phone": phone_number}
            return Response(response)

        except User.DoesNotExist:
            raise NotFound(detail="اطلاعات وارد شده اشتباه است")

    # Verify otp
    @action(methods=["post"], detail=False)
    def verify_code(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Checking the presence or absence of user
        try:
            user = User.objects.get(phone_number=data["phone_number"])
        except User.DoesNotExist:
            raise NotFound("کاربر با این اطلاعات وجود ندارد")

        # Checking otp expire time
        code = redis.get(f"user_{user.id}_otp")
        if code is None:
            raise PermissionDenied("کد منقضی شده است")

        # Checking otp value
        if code.decode("utf-8") == data["code"]:
            token = TokenObtainPairSerializer(
                data={
                    "phone_number": data["phone_number"],
                }
            )
            token.is_valid(raise_exception=True)
            return Response(VerifyCodeResponseSerializer(token.validated_data).data)
        else:
            raise NotAcceptable("کد وارد شده صحیح نمی‌باشد")


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
