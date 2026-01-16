"""
Custom permissions for LegalDocs Manager API.

Provides permission classes for controlling access to API resources
based on object ownership and user roles.
"""

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of a document to delete it.

    - Read permissions (GET, HEAD, OPTIONS) are allowed for any authenticated request.
    - Write permissions (PUT, PATCH) are allowed for any authenticated request.
    - Delete permissions are only allowed for the document owner or staff users.
    """

    def has_object_permission(self, request, view, obj):
        """Check if the user has permission to perform the action on the object."""
        # Read permissions are allowed for any authenticated request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions (except DELETE) are allowed for any authenticated user
        if request.method in ['PUT', 'PATCH']:
            return True

        # Delete permission only for owner or admin
        if request.method == 'DELETE':
            return obj.uploaded_by == request.user or request.user.is_staff

        return True
