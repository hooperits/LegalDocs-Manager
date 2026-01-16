"""
Serializers for the API app.

Provides serializers for authentication, user profile, and search functionality.
"""

from django.contrib.auth.models import User
from rest_framework import serializers


class UserInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for basic user information.

    Used by /auth/me/ endpoint to return current user data.
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id', 'username']


class RegisterSerializer(serializers.Serializer):
    """
    Serializer for user registration.

    Validates username uniqueness and password confirmation.
    Creates a new user on successful validation.
    """

    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)

    def validate_username(self, value):
        """Check that username is not already taken."""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value

    def validate(self, data):
        """Validate that passwords match."""
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"non_field_errors": ["Passwords do not match."]})
        return data

    def create(self, validated_data):
        """Create and return a new user."""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile with assigned cases count.

    Used by /profile/ endpoint for viewing and updating user profile.
    Username and date_joined are read-only.
    """

    assigned_cases_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'assigned_cases_count',
            'date_joined'
        ]
        read_only_fields = ['id', 'username', 'date_joined', 'assigned_cases_count']

    def get_assigned_cases_count(self, obj):
        """Return count of cases assigned to this user."""
        from cases.models import Case
        return Case.objects.filter(assigned_to=obj).count()
