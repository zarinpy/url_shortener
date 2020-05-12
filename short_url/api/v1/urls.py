from rest_framework.routers import SimpleRouter

from .views import ShortUrlViewSet, DashboardViewSet

app_name = 'short_url'

router = SimpleRouter()
router.register('', ShortUrlViewSet, basename='shortener')
router.register('dashboard', DashboardViewSet, basename='dashboard')
urlpatterns = router.urls
