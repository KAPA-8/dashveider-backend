# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from .models import Organization, UserProfile
from .serializers import OrganizationSerializer, UserSerializer, UserCreateSerializer

User = get_user_model()


class OrganizationListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        """Use different serializers for Radical users vs regular users"""
        if self.request.method == "POST":
            try:
                user_profile = self.request.user.organization_profile
                if user_profile.can_create_organizations:
                    return OrganizationSerializer
                else:
                    raise PermissionDenied(
                        "Only Radical organization users can create new organizations"
                    )
            except UserProfile.DoesNotExist:
                raise PermissionDenied("User must be linked to an organization")
        return OrganizationSerializer

    def get_queryset(self):
        """Return organizations based on user permissions"""
        try:
            user_profile = self.request.user.organization_profile
            if user_profile.can_create_organizations:
                # Radical users can see all organizations
                return Organization.objects.all()
            else:
                # Regular users can only see their own organization
                return Organization.objects.filter(id=user_profile.organization.id)
        except UserProfile.DoesNotExist:
            return Organization.objects.none()

    def create(self, request, *args, **kwargs):
        """Create organization (only for Radical users)"""
        try:
            user_profile = request.user.organization_profile
            if not user_profile.can_create_organizations:
                return Response(
                    {
                        "error": "Only Radical organization users can create new organizations"
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )
        except UserProfile.DoesNotExist:
            return Response(
                {"error": "User must be linked to an organization"},
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().create(request, *args, **kwargs)


class OrganizationRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Organization.objects.all()

    def get_object(self):
        """Check permissions for organization access"""
        obj = super().get_object()

        try:
            user_profile = self.request.user.organization_profile

            # Radical users can access any organization
            if user_profile.can_create_organizations:
                return obj

            # Regular users can only access their own organization
            if obj.id == user_profile.organization.id:
                return obj

            raise PermissionDenied("You do not have access to this organization")

        except UserProfile.DoesNotExist:
            raise PermissionDenied("User must be linked to an organization")

    def update(self, request, *args, **kwargs):
        """Handle different update permissions"""
        obj = self.get_object()
        user_profile = request.user.organization_profile

        # For regular organizations, prevent updating certain fields
        if (
            not user_profile.can_create_organizations
            and obj.id == user_profile.organization.id
        ):
            # Regular org users can't change name, employees_count
            protected_fields = ["name", "employees_count"]
            for field in protected_fields:
                if field in request.data:
                    return Response(
                        {"error": f"You cannot modify the '{field}' field"},
                        status=status.HTTP_403_FORBIDDEN,
                    )

        return super().update(request, *args, **kwargs)


class OrganizationUsersListCreateView(generics.ListCreateAPIView):
    """Manage users within an organization"""

    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserCreateSerializer
        return UserSerializer

    def get_queryset(self):
        """Return users based on organization permissions"""
        organization_id = self.kwargs["organization_id"]

        try:
            user_profile = self.request.user.organization_profile

            # Check if user can access this organization
            if user_profile.can_create_organizations:
                # Radical users can see users of any organization
                organization = Organization.objects.get(id=organization_id)
            elif user_profile.organization.id == organization_id:
                # Regular users can only see users of their own organization
                organization = user_profile.organization
            else:
                raise PermissionDenied(
                    "You do not have access to this organization's users"
                )

            # Return users linked to this organization
            user_profiles = UserProfile.objects.filter(organization=organization)
            user_ids = user_profiles.values_list("user_id", flat=True)
            return User.objects.filter(id__in=user_ids)

        except (UserProfile.DoesNotExist, Organization.DoesNotExist):
            return User.objects.none()

    def perform_create(self, serializer):
        """Create user and link to organization"""
        organization_id = self.kwargs["organization_id"]

        try:
            user_profile = self.request.user.organization_profile

            # Check permissions - only Radical users can create users for any organization
            if user_profile.can_create_organizations:
                organization = Organization.objects.get(id=organization_id)
            else:
                raise PermissionDenied(
                    "Only Radical organization users can create users for organizations"
                )

            # Create user
            user = serializer.save()

            # Link to organization
            UserProfile.objects.create(user=user, organization=organization)

        except (UserProfile.DoesNotExist, Organization.DoesNotExist):
            raise PermissionDenied("Invalid organization or user permissions")


class OrganizationUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Manage individual users within an organization"""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        organization_id = self.kwargs["organization_id"]

        try:
            user_profile = self.request.user.organization_profile

            # Check if user can access this organization
            if user_profile.can_create_organizations:
                organization = Organization.objects.get(id=organization_id)
            elif user_profile.organization.id == organization_id:
                organization = user_profile.organization
            else:
                return User.objects.none()

            user_profiles = UserProfile.objects.filter(organization=organization)
            user_ids = user_profiles.values_list("user_id", flat=True)
            return User.objects.filter(id__in=user_ids)

        except (UserProfile.DoesNotExist, Organization.DoesNotExist):
            return User.objects.none()
