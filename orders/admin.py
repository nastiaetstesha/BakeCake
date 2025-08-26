from django.contrib import admin
from .models import Order, OrderItem, OrderItemBerry, OrderItemDecor


class OrderItemBerryInline(admin.TabularInline):
    model = OrderItemBerry
    extra = 0


class OrderItemDecorInline(admin.TabularInline):
    model = OrderItemDecor
    extra = 0


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0
    inlines = [OrderItemBerryInline, OrderItemDecorInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'status', 'contact_name', 'phone', 'total', 'utm_source', 'utm_medium')
    list_filter = ('status', 'created_at', 'utm_source', 'utm_medium')
    search_fields = ('contact_name', 'phone', 'email', 'city', 'street')
    inlines = [OrderItemInline]
