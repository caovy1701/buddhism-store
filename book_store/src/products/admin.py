from django.contrib import admin

# Register your models here.

from src.products.models import Product, Category, ProductVariant, Media


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]

class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]

class MediaAdmin(admin.ModelAdmin):
    list_display = ['id', 'file', ]

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)
admin.site.register(Media, MediaAdmin)