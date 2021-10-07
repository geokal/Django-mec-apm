from django.urls import path, include
from rest_framework.routers import DefaultRouter
from AppPackageManagement import views

router = DefaultRouter()
router.register(r'app_packages', views.AppPackagesViewSet)

urlpatterns = [
    path('app_pkgm/v1/', include(router.urls)),
]