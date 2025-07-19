import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticated_client(api_client):
    def get_client(user=None):
        if not user:
            user = User.objects.create_user(
                email='test@user.com',
                password='testpass123'
            )
        api_client.force_authenticate(user=user)
        return api_client
    return get_client

@pytest.fixture
def admin_client(api_client):
    admin = User.objects.create_superuser(
        email='admin@test.com',
        password='adminpass123'
    )
    api_client.force_authenticate(user=admin)
    return api_client