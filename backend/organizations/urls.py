from django.urls import path

from .views import (
    OrganizationListCreateView,
    OrganizationRetrieveUpdateView,
    OrganizationUsersListCreateView,
    OrganizationUserDetailView,
)


urlpatterns = [
    path("", OrganizationListCreateView.as_view(), name="organization-list-create"),
    path(
        "<int:pk>/",
        OrganizationRetrieveUpdateView.as_view(),
        name="organization-detail",
    ),
    path(
        "<int:organization_id>/users/",
        OrganizationUsersListCreateView.as_view(),
        name="organization-users-list-create",
    ),
    path(
        "<int:organization_id>/users/<int:pk>/",
        OrganizationUserDetailView.as_view(),
        name="organization-user-detail",
    ),
]
