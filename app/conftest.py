import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.fixture
def api_client(db):
    user, _ = User.objects.get_or_create(
        username="User", first_name="Anonymous", last_name="User"
    )
    client = APIClient()
    client.force_authenticate(user=user)
    return client
