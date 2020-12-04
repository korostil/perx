from rest_framework import routers

from analytics.views import ReportViewSet

router = routers.SimpleRouter()
router.register('reports', ReportViewSet)

urlpatterns = router.urls
