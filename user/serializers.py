from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models.Address import Address

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        write_only=True,
        required=False
    )

    class Meta:
        model = User
        fields = ["id", "image", "first_name", "last_name", "is_active", "date_joined", 'get_full_name', "email", "phone_number", "username", "address", "national_code", "is_admin", "images"]
        depth = 1


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="ایمیل توسط کاربر دیگری استفاده شده است.")]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True
    )
    phone_number = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="شماره تلفن شما موجود هست")],
    )

    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="نام کاربری توسط کاربر دیگری استفاده شده است.")]
    )

    class Meta:
        model = User
        fields = ("phone_number", 'username', 'password', 'password2', 'email')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            phone_number=validated_data['phone_number']
        )
        user.username = validated_data['username']
        user.set_password(validated_data['password'])
        user.save()

        return user


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["id", 'city', 'rest_of', "owner"]



