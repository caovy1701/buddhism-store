from django.contrib import admin
from src.products.models import (
    Category,
    GenericActivity,
    Media,
    Product,
    ProductVariant,
)

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
    ]


class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
    ]


class ProductVariantAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
    ]


class MediaAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "file",
    ]


class GenericActivityAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "content_type",
        "object_id",
        "type",
    ]


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(GenericActivity, GenericActivityAdmin)
