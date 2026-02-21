import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestLogin:
    url = reverse("login")

    def test_login_success(self, api_client, user):
        data = {"email": user.email, "password": "testpass123"}
        response = api_client.post(self.url, data)

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_login_wrong_password(self, api_client, user):
        data = {"email": user.email, "password": "wrongpass"}
        response = api_client.post(self.url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_inactive_user(self, api_client, user):
        user.is_active = False
        user.save()

        data = {"email": user.email, "password": "testpass123"}
        response = api_client.post(self.url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
