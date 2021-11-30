from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['get_full_name', "phone_number", "username", "address", "national_code", "is_admin", "images"]
