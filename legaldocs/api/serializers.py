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


class CustomAuthTokenSerializer(serializers.Serializer):
    """
    Custom auth token serializer that explicitly passes the request object
    to django's authenticate() function to ensure axes lockout logic operates.
    """

    username = serializers.CharField(
        label=serializers.Field.default_error_messages.get('required', 'Username'),
        write_only=True
    )
    password = serializers.CharField(
        label=serializers.Field.default_error_messages.get('required', 'Password'),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label='Token',
        read_only=True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            from django.contrib.auth import authenticate
            from django.utils.translation import gettext_lazy as _
            from axes.handlers.proxy import AxesProxyHandler
            from rest_framework.exceptions import PermissionDenied

            request = self.context.get('request')

            if request:
                credentials = {'username': username}
                if not AxesProxyHandler.is_allowed(request, credentials):
                    request.axes_locked_out = True
                    request.axes_credentials = credentials
                    if hasattr(request, '_request'):
                        request._request.axes_locked_out = True
                        request._request.axes_credentials = credentials
                    raise PermissionDenied()

            try:
                user = authenticate(request=request, username=username, password=password)
            except Exception:
                raise

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')

            # Reset axes failed attempts count on successful login
            from axes.utils import reset
            reset(username=username)
        else:
            from django.utils.translation import gettext_lazy as _
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

