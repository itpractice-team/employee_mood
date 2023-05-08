from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Department, Position, User


class DepartmentAdmin(admin.ModelAdmin):
    pass


class PositionAdmin(admin.ModelAdmin):
    pass


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'password')}),
        (('Служебная информация'), {'fields': (
            'department', 'position', 'role', 'avatar', 'phone'
        )}),
        (('Роли и права'), {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
        (('Даты'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name',
                       'password1', 'password2'
                       ),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'role', 'department')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(User, CustomUserAdmin)
