from rest_framework.routers import SimpleRouter

from .views import RegisterViewSet

app_name = 'accounts'

router = SimpleRouter()
router.register('', RegisterViewSet, basename='register')
urlpatterns = router.urls
