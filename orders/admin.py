from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('line_subtotal',)
    autocomplete_fields = ('levels', 'shape', 'topping', 'berry', 'decor', 'cake')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','created_at','status','contact_name','phone','total')
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id','order','cake','levels','shape','topping','berry','decor','line_subtotal')
    readonly_fields = ('line_subtotal',)
    autocomplete_fields = ('levels','shape','topping','berry','decor','cake')
