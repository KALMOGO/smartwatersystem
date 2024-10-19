from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import ValidationError
from .models import User


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=280)
    tel = serializers.CharField(max_length=250)
    photo = serializers.CharField(max_length=260)
    password = serializers.CharField(min_length=8)

    class Meta:
        model = User
        fields = [
            "email", "photo", "password", "first_name", "last_name","tel"
        ]

    def validate(self, attrs):

        if email_exists := User.objects.filter(email=attrs["email"]).exists():
            raise ValidationError("Email has already been used")

        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =( 'id', "first_name", "last_name", "email","photo","tel" )