
from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('items', views.ItemViewSet, basename='items')
router.register('categories', views.CategoryViewSet)
router.register('stations', views.StationViewSet)
router.register('users', views.UserViewSet)
router.register('truck', views.TruckViewSet)
router.register('remittance', views.RemittanceViewSet)
router.register('orders', views.OrderViewSet)
router.register('supply', views.SupplyViewSet)

urlpatterns = router.urls 