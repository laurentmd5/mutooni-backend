from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from users.models import User

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display  = ("username", "email", "role", "is_active", "is_staff")
    list_filter   = ("role", "is_staff", "is_active")
    search_fields = ("username", "email")
    fieldsets     = DjangoUserAdmin.fieldsets + (
        ("Rôle & Permissions", {"fields": ("role",)}),
    )
