import pytest
from django.urls import reverse
from rest_framework import status

from ..models import User


@pytest.mark.django_db
class TestRegistration:
    url = reverse("register")

    def test_register_success(self, api_client):
        data = {
            "email": "newuser@example.com",
            "password": "newpass123",
            "first_name": "New",
            "last_name": "User",
        }
        response = api_client.post(self.url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert "access" in response.data
        assert "refresh" in response.data
        assert User.objects.filter(email="newuser@example.com").exists()

    def test_register_email_exists(self, api_client, user):
        data = {
            "email": user.email,
            "password": "newpass123",
            "first_name": "New",
            "last_name": "User",
        }
        response = api_client.post(self.url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data

    def test_register_short_password(self, api_client):
        data = {
            "email": "short@example.com",
            "password": "123",
            "first_name": "Short",
            "last_name": "User",
        }
        response = api_client.post(self.url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password" in response.data
