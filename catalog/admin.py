from django.contrib import admin
from .models import OptionCategory, Option


@admin.register(OptionCategory)
class OptionCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'multi_select')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price_delta', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name',)
