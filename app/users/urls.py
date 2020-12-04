from django.conf.urls import url

from users.views import login_view, logout_view, CustomAuthToken

urlpatterns = [
    url('token/', CustomAuthToken.as_view(), name='token_obtain'),
    url('login/', login_view, name='login'),
    url('logout/', logout_view, name='logout'),
]
