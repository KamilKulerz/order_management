from django.urls import include, path
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'customers', views.CustomerViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'items', views.ItemViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
