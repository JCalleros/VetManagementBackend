from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    password2 = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password',
                  'password2', 'phone_number', 'role', 'profile_image']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'password2': {'write_only': True, 'required': False}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        password2 = validated_data.pop('password2', None)
        if password and password2:
            if password != password2:
                raise serializers.ValidationError({"password": "Password fields didn't match."})
            user = CustomUser(**validated_data)
            user.set_password(password)
            user.save()
            return user
        else:
            raise serializers.ValidationError({"password": "Password fields are required."})

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        password2 = validated_data.pop('password2', None)
        if password or password2:
            raise serializers.ValidationError({"password": "Password fields are not allowed in update."})
        return super().update(instance, validated_data)
