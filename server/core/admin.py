from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, CustomerProfile, RestaurantProfile, RiderProfile,
    MenuItem, Order, OrderItem, Payment, Review, Subscription, Address
)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone_number', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'groups')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('phone_number', 'user_type')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('phone_number', 'user_type')}),
    )

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'default_address')
    search_fields = ('user__username', 'user__email')

@admin.register(RestaurantProfile)
class RestaurantProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'cuisine_type', 'is_active')
    list_filter = ('cuisine_type', 'is_active')
    search_fields = ('name', 'description')

@admin.register(RiderProfile)
class RiderProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'vehicle_type', 'license_number', 'is_active')
    list_filter = ('vehicle_type', 'is_active')
    search_fields = ('user__username', 'license_number')

class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'price', 'category', 'is_available')
    list_filter = ('restaurant', 'category', 'is_available')
    search_fields = ('name', 'description', 'restaurant__name')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('item_price',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'menu_item', 'quantity', 'item_price')
    list_filter = ('order__status',)
    search_fields = ('order__id', 'menu_item__name')
    readonly_fields = ('item_price',)
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'restaurant', 'rider', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer__user__username', 'restaurant__name', 'rider__user__username')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [OrderItemInline]

    fieldsets = (
        ('Order Info', {'fields': ('customer', 'restaurant', 'rider', 'status', 'total_amount')}),
        ('Delivery Details', {'fields': ('delivery_address', 'delivery_instructions')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('customer', 'restaurant', 'rider')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method')
    search_fields = ('order__id', 'transaction_id')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('order', 'customer', 'restaurant', 'rider', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('customer__user__username', 'restaurant__name', 'comment')
    readonly_fields = ('created_at',)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('customer', 'plan_type', 'start_date', 'end_date', 'status')
    list_filter = ('plan_type', 'status')
    search_fields = ('customer__user__username',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'street', 'city', 'state', 'country', 'postal_code', 'is_default')
    list_filter = ('is_default', 'city', 'state', 'country')
    search_fields = ('user__username', 'street', 'city')