from main.models import User, Thesis, Message
from django.contrib.auth.models import update_last_login
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import NotAuthenticated
from rest_framework_simplejwt.authentication import api_settings
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as JWTTokenObtainPairSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
        ]


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    ssn = serializers.CharField(required=True)
    national_code = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "ssn",
            "national_code",
            "password",
        ]


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)


class TokenObtainPairSerializer(JWTTokenObtainPairSerializer):
    token_class = RefreshToken

    # Override get_token for extra token claims
    @classmethod
    def get_token(self, user):
        token = super().get_token(user)

        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        token["phone_number"] = user.phone_number
        token["email"] = user.email
        token["role"] = user.get_role_display()

        return token

    # Override validate
    def validate(self, attrs):
        authenticate_kwargs = {
            "username": attrs["username"],
            "password": attrs["password"],
        }

        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        # Change authentication system
        try:
            self.user = User.objects.get(username=authenticate_kwargs["username"])
            self.user.check_password(authenticate_kwargs["password"])
        except User.DoesNotExist:
            raise NotAuthenticated

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )

        data = {}

        # Generate token
        refresh = self.get_token(self.user)
        data["token"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "ssn",
            "national_code",
        ]


class ThesisSerializer(serializers.ModelSerializer):
    teacher = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field="ssn",
    )
    refree = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field="ssn",
    )

    class Meta:
        model = Thesis
        fields = "__all__"
        read_only_fields = ["student"]


class ThesisResponseSerializer(serializers.ModelSerializer):
    teacher = serializers.CharField(source="teacher.full_name")
    refree = serializers.CharField(source="refree.full_name")
    student = serializers.CharField(source="student.full_name")

    class Meta:
        model = Thesis
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    reciever = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field="ssn"
    )
    sender = serializers.CharField(source="sender.full_name")

    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = ["sender"]
