import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestProfile:
    url = reverse("profile")

    def test_get_profile(self, auth_client):
        response = auth_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert "email" in response.data
        assert "first_name" in response.data
        assert "last_name" in response.data

    def test_update_profile(self, auth_client):
        data = {"first_name": "Updated", "last_name": "Name"}
        response = auth_client.put(self.url, data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["first_name"] == "Updated"
        assert response.data["last_name"] == "Name"

    def test_profile_unauthorized(self, api_client):
        response = api_client.get(self.url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
