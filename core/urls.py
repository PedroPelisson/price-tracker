from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, UserCreateView

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('', include(router.urls)),
]