from rest_framework import serializers

from .models import User


class UserSerializer(serializers.Serializer):
    id = serializers.CharField(read_only = True)
    username = serializers.CharField(max_length = 32)
    email = serializers.EmailField()
    password = serializers.CharField(write_only = True)

    def validate_username(self, value):
        if User.objects(username = value).first():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_email(self, value):
        if User.objects(email = value).first():
            raise serializers.ValidationError("Email already exists")
        return value

    def create(self, validated_data):
        user = User(
            username = validated_data['username'],
            email    = validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only = True)
