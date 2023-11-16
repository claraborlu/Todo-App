from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email does not exist.")
        return value

    def save(self):
        request = self.context.get('request')
        options = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
        }
        reset_form = PasswordResetForm(data=self.validated_data)
        if reset_form.is_valid():
            reset_form.save(**options)