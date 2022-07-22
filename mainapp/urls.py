from rest_framework import routers
from mainapp.views import AuthView, UserViewSet, QuotaViewSet, ResourceViewSet
from django.urls import path


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'quotas', QuotaViewSet)
router.register(r'resources', ResourceViewSet)


urlpatterns = [
    path('auth/', AuthView.as_view(), name="auth_api_view"),
]


urlpatterns += router.urls
