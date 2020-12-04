import pytest
from django.conf import settings


@pytest.fixture(scope='module', autouse=True)
def patch_settings():
    settings.SERVICE_USER = 'test_user'
    settings.SERVICE_PASSWORD = 'test_password'
