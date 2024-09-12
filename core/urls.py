from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CustomerProfileViewSet, RestaurantProfileViewSet, RiderProfileViewSet, MenuItemViewSet, OrderViewSet, PaymentViewSet, ReviewViewSet, SubscriptionViewSet, AddressViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'customers', CustomerProfileViewSet)
router.register(r'restaurants', RestaurantProfileViewSet)
router.register(r'riders', RiderProfileViewSet)
router.register(r'menu-items', MenuItemViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'addresses', AddressViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]