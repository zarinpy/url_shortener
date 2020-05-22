from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from short_url.api.v1.views import RedirectToView

api_v1 = [
    path('register/', include('accounts.api.v1.urls'), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('home/', include('short_url.api.v1.urls'), name='url_creator'),
]
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include((api_v1, 'url_shortener'), namespace='url_shortener')),
    path(r'r/<str:input_url>/', RedirectToView.as_view(), name='shorted'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
