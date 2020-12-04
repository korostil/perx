from django.conf.urls import url, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    url('api/analytics/', include('analytics.urls')),
    url('api/users/', include('users.urls')),
    url(r'^$', schema_view.with_ui('swagger', cache_timeout=0)),
]
