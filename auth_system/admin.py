from django.contrib import admin
from .models import User, Role, UserRole, BusinessObject, AccessRoleRule, Session


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "created_at",
    )
    list_filter = ("is_active", "is_staff", "created_at")
    search_fields = ("email", "first_name", "last_name")
    readonly_fields = ("created_at", "update_at")


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name", "description")


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "assigned_at")
    list_filter = ("role", "assigned_at")
    search_fields = ("user__email", "role__name")


@admin.register(BusinessObject)
class BusinessObjectAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code", "description")


@admin.register(AccessRoleRule)
class AccessRoleRuleAdmin(admin.ModelAdmin):
    list_display = (
        "role",
        "business_object",
        "read_permission",
        "read_all_permission",
        "create_permission",
        "update_permission",
        "update_all_permission",
        "delete_permission",
        "delete_all_permission",
    )
    list_filter = ("role", "business_object")
    list_editable = (
        "read_permission",
        "read_all_permission",
        "create_permission",
        "update_permission",
        "update_all_permission",
        "delete_permission",
        "delete_all_permission",
    )


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("user", "expires_at", "created_at")
    list_filter = ("expires_at", "created_at")
    search_fields = ("user__email", "token")
