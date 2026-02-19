import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
class TestLogout:
    url = reverse("logout")

    def test_logout_success(self, auth_client, user):
        refresh = RefreshToken.for_user(user)
        data = {"refresh": str(refresh)}
        
        response = auth_client.post(self.url, data)
        
        assert response.status_code == status.HTTP_200_OK

    def test_logout_invalid_token(self, auth_client):
        data = {"refresh": "invalid_token"}
        
        response = auth_client.post(self.url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
