from rest_framework import serializers
from .models import User, CustomerProfile, RestaurantProfile, RiderProfile, MenuItem, Order, OrderItem, Payment, Review, Subscription, Address

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'user_type']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'street', 'city', 'state', 'country', 'postal_code', 'is_default']

class CustomerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = CustomerProfile
        fields = ['id', 'user', 'addresses']

class RestaurantProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = RestaurantProfile
        fields = ['id', 'user', 'name', 'description', 'cuisine_type', 'address', 'latitude', 'longitude', 'operating_hours', 'is_active']

class RiderProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = RiderProfile
        fields = ['id', 'user', 'vehicle_type', 'license_number', 'is_active']

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'restaurant', 'name', 'description', 'price', 'category', 'is_available', 'image_url']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'quantity', 'item_price', 'special_instructions']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'restaurant', 'rider', 'status', 'total_amount', 'delivery_address', 'delivery_instructions', 'items', 'created_at', 'updated_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'order', 'amount', 'payment_method', 'transaction_id', 'status', 'created_at', 'updated_at']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'order', 'customer', 'restaurant', 'rider', 'rating', 'comment', 'created_at']

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'customer', 'plan_type', 'start_date', 'end_date', 'status', 'created_at', 'updated_at']