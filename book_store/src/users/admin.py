from django.contrib import admin
from src.users.models import User, Address

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
    ]
    search_fields = ["email", "first_name", "last_name"]
    list_filter = ["is_active", "is_staff", "is_superuser"]
    list_editable = ["is_active", "is_staff", "is_superuser"]
    list_per_page = 20
    # hide password
    fieldsets = (
        ("Personal info", {"fields": ("first_name", "last_name", "phone_number")}),
        (
            "Permissions",
            {"fields": ("is_active", "is_staff", "is_superuser", "is_owner")},
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    ordering = ["email"]


admin.site.register(User, UserAdmin)
admin.site.register(Address)
