from django.contrib import admin
from .models import OptionCategory, Option, Cake, CakeImage


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


class CakeImageInline(admin.TabularInline):
    model = CakeImage
    extra = 0


@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'from_price', 'weight_grams', 'servings', 'is_active'
        )
    list_filter = ('is_active',)
    search_fields = ('title', 'short_description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('available_fillings',)
    inlines = [CakeImageInline]