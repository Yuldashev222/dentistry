from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, exceptions

from .models import CustomUser, Answer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'is_staff', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'validators': [validate_password]}
        }

    def create(self, validated_data):
        instance = CustomUser.objects.create_user(**validated_data)
        return instance


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

    def validate_client(self, client):
        if client.is_staff:
            raise exceptions.ValidationError('select a client')
        return client
