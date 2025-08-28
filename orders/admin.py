from django.contrib import admin
from django import forms

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


class OrderItemForm(forms.ModelForm):
    inscription_text = forms.CharField(
        label='Надпись (необязательно)',
        required=False,
        help_text='Мы можем разместить на торте любую надпись, например: «С днём рождения!». Доплата добавится автоматически.'
    )

    class Meta:
        model = OrderItem
        fields = '__all__'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'status', 'contact_name', 'phone', 'total', 'utm_source', 'utm_medium')
    list_filter = ('status', 'created_at', 'utm_source', 'utm_medium')
    search_fields = ('contact_name', 'phone', 'email', 'city', 'street')
    inlines = [OrderItemInline]
