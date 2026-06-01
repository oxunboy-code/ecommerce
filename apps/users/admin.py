from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'role', 'is_staff', 'date_joined')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('-date_joined',)

    fieldsets = UserAdmin.fieldsets + (
        ('Qo\'shimcha', {'fields' : ('role', 'phone', 'avatar')}),
    )