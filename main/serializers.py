from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, exceptions

from .models import CustomUser, Answer, Order, Message


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


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['creator']

    def validate(self, attrs):
        user = self.context['request'].user
        if not user.is_staff and user.id != attrs['answer'].order.client.id:
            raise exceptions.NotFound({'answer': 'Not Found'})
        return attrs


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['number', 'client']

    def create(self, validated_data):
        return Order.objects.create(**validated_data)
