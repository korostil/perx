import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.parametrize('password,expected', [('test_password', 200), ('', 403)])
def test_login(api_client, password, expected):
    response = api_client.post(reverse('login'), data={'username': 'test_user', 'password': password})

    assert response.status_code == expected


@pytest.mark.parametrize('logged_in,expected', [(True, 200), (False, 403)])
def test_token(api_client, logged_in, expected):
    user, _ = User.objects.get_or_create(username='User', first_name='Anonymous', last_name='User')
    token, _ = Token.objects.get_or_create(user=user)
    if logged_in:
        api_client.force_authenticate(user)
    else:
        api_client.force_authenticate(None)

    response = api_client.post(reverse('token_obtain'))

    assert response.status_code == expected
    if response.status_code == 200:
        assert 'token' in response.data


@pytest.mark.parametrize('logged_in,expected', [(True, 200), (False, 403)])
def test_logout(api_client, logged_in, expected):
    if logged_in:
        user, _ = User.objects.get_or_create(username='User', first_name='Anonymous', last_name='User')
        api_client.force_authenticate(user)
    else:
        api_client.force_authenticate(None)

    response = api_client.post(reverse('logout'))

    assert response.status_code == expected

