import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
class TestDeleteAccount:
    url = reverse("delete_account")

    def test_delete_account(self, auth_client, user):
        response = auth_client.post(self.url)
        
        assert response.status_code == status.HTTP_200_OK
        user.refresh_from_db()
        assert user.is_active is False

    def test_delete_account_with_logout(self, auth_client, user):
        refresh = RefreshToken.for_user(user)
        data = {"refresh": str(refresh)}
        
        response = auth_client.post(self.url, data)
        
        assert response.status_code == status.HTTP_200_OK
        user.refresh_from_db()
        assert user.is_active is False
