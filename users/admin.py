from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_instructor', 'is_staff', 'date_joined')
    list_filter = ('is_instructor', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información Personal', {'fields': ('first_name', 'last_name', 'avatar', 'bio')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_instructor', 'groups', 'user_permissions')}),
        ('Fechas Importantes', {'fields': ('last_login',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'country', 'city')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'phone')
    list_filter = ('country',)
