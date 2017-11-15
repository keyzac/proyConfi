from django.contrib.auth import authenticate, login
from requests.exceptions import HTTPError
from rest_framework.authtoken.models import Token
from .models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail.message import EmailMessage
from requests.exceptions import HTTPError
from django.template import loader
from django.conf import settings
from rest_framework import serializers
from social.exceptions import AuthCanceled


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name',)
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(email=validated_data['email'], first_name=validated_data['first_name'],
                                   last_name=validated_data['last_name'])
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(error_messages={"blank": "Este campo es obligatorio"})
    password = serializers.CharField(error_messages={"blank": "Este campo es obligatorio"})

    def validate(self, attrs):
        self.user_cache = authenticate(email=attrs["email"], password=attrs["password"])
        if not self.user_cache:
            raise serializers.ValidationError("Invalid login")
        else:
            return attrs

    def get_user(self):
        return self.user_cache


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(error_messages={"blank": "Este campo es obligatorio"})
    new_password = serializers.CharField(error_messages={"blank": "Este campo es obligatorio"})
    email = serializers.EmailField(error_messages={"blank": "Este campo es obligatorio"})

    def validate(self, attrs):
        user = self.context.get("user")
        if attrs.get("email") != user.email:
            raise serializers.ValidationError({"email": "Email mismatch"})
        if not user.check_password(attrs.get("old_password")):
            raise serializers.ValidationError({"password": "Password mismatch"})
        return attrs

    def save(self, **kwargs):
        user = self.context.get("user")
        user.set_password(self.validated_data.get("new_password"))
        user.save()


class ResetPasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("Both password have to be the same")
        return data

    def save(self, user):
        user.set_password(self.validated_data.get('password1'))
        user.save()


class PasswordRecoverySerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        self.cached_user = User.objects.filter(email=value).first()
        if not self.cached_user:
            raise serializers.ValidationError("The email is not registered")
        return value

    def save(self):
        to_email = self.validated_data.get("email")
        id = self.cached_user.pk
        token = default_token_generator.make_token(self.cached_user)
        request = self.context.get("request")
        domain = get_current_site(request).domain
        protocol = 'https' if request.is_secure() else 'http'
        print(protocol)
        context = {
            'id': id,
            'token': token,
            'domain': domain,
            'protocol': protocol
        }
        html_user = loader.get_template("accounts/mail/password_reset.html")
        user_context_html = html_user.render(context)
        subject_user, from_email = 'Cambiar Contraseña', settings.CONTACT_EMAIL
        message_user = EmailMessage(subject_user, user_context_html, from_email, [to_email])
        print(to_email)
        message_user.content_subtype = "html"
        message_user.send(fail_silently=True)


class RetrieveUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'picture',)
        read_only_fields = ('id', 'email',)


class FacebookLoginSerializer(serializers.Serializer):
    access_token = serializers.CharField(
        error_messages={"blank": "Este campo es obligatorio"})

    def validate(self, attrs):
        request = self.context.get("request")
        self.user_cache = None
        try:
            self.user_cache = request.backend.do_auth(attrs.get("access_token"))
            return attrs
        except HTTPError:
            raise serializers.ValidationError("Invalid facebook token")

    def get_user(self):
        return self.user_cache


class UserFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'picture')


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class UpdateUserPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('picture',)


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name',)