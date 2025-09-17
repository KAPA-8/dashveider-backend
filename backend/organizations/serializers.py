from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Organization, UserProfile

User = get_user_model()


class OrganizationSerializer(serializers.ModelSerializer):
    """Serializer for organization management"""

    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
            "logo_url",
            "description",
            "document_number",
            "issues",
            "employees_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating users within an organization"""

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "is_active",
            "date_joined",
        ]
        read_only_fields = ["id", "date_joined"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user management within organizations"""

    organization_name = serializers.CharField(
        source="organization_profile.organization.name", read_only=True
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "date_joined",
            "organization_name",
        ]
        read_only_fields = ["id", "email", "date_joined", "organization_name"]
