from django.contrib import admin
from .models import Customer, Address


class AddressInline(admin.TabularInline):
    model = Address
    extra = 0

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'created_at')
    inlines = [AddressInline]

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('customer', 'city', 'street', 'house', 'is_default')
    list_filter = ('city', 'is_default')
