from django.contrib import admin
from .models import PromoCode


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'amount', 'active', 'valid_from', 'valid_until', 'used_count', 'max_uses')
    list_filter = ('active', 'discount_type')
    search_fields = ('code',)
