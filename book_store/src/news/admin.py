from django.contrib import admin
from .models import News, Category

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "description"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name", "slug"]
    list_filter = ["created", "modified"]
    list_per_page = 20


class NewsAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "category", "created"]
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ["title", "slug", "content"]
    list_filter = ["created", "modified"]
    list_per_page = 20


admin.site.register(Category, CategoryAdmin)
admin.site.register(News, NewsAdmin)
