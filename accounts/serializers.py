from django.contrib.auth import get_user_model  # Для подключения к API пользователей
from rest_framework import serializers
from .models import ProfileData, VerificationData, AvatarData


class UserSerializer(serializers.ModelSerializer):  # Для подключения к API пользователей
    class Meta:
        model = get_user_model()
        fields = ('id', 'username',)


class ProfileDataSerializer(serializers.ModelSerializer):  # Для подключения к API пользователей
    class Meta:
        model = ProfileData
        fields = ('id', 'username', 'telephone', 'telephone_verified')
        extra_kwargs = {'username': {'required': False}}
        lookup_field = 'username'


class AvatarDataSerializer(serializers.ModelSerializer):  # Для подключения к API пользователей
    class Meta:
        model = AvatarData
        fields = ('username', 'avatar',)
        extra_kwargs = {'username': {'required': False}}
        lookup_field = 'username'


class VerificationPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationData
        fields = ('profile', 'request_id', 'code',)
        extra_kwargs = {'request_id': {'required': False}}

