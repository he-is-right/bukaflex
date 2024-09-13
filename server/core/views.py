# from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, CustomerProfile, RestaurantProfile, RiderProfile, MenuItem, Order, Payment, Review, Subscription, Address
from .serializers import UserSerializer, CustomerProfileSerializer, RestaurantProfileSerializer, RiderProfileSerializer, MenuItemSerializer, OrderSerializer, PaymentSerializer, ReviewSerializer, SubscriptionSerializer, AddressSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class CustomerProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class RestaurantProfileViewSet(viewsets.ModelViewSet):
    queryset = RestaurantProfile.objects.all()
    serializer_class = RestaurantProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type == 'restaurant_owner':
            return self.queryset.filter(user=self.request.user)
        return self.queryset.filter(is_active=True)

class RiderProfileViewSet(viewsets.ModelViewSet):
    queryset = RiderProfile.objects.all()
    serializer_class = RiderProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type == 'rider':
            return self.queryset.filter(user=self.request.user)
        return self.queryset.none()

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        restaurant_id = self.request.query_params.get('restaurant_id')
        if restaurant_id:
            return self.queryset.filter(restaurant_id=restaurant_id, is_available=True)
        return self.queryset.filter(is_available=True)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'customer':
            return self.queryset.filter(customer__user=user)
        elif user.user_type == 'restaurant_owner':
            return self.queryset.filter(restaurant__user=user)
        elif user.user_type == 'rider':
            return self.queryset.filter(rider__user=user)
        return self.queryset.none()

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer_profile)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(order__customer__user=self.request.user)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer_profile)

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(customer__user=self.request.user)

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)