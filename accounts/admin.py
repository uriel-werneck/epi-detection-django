from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = ('email', 'email_confirmado', 'nome', 'sobrenome', 'telefone', 'is_staff', 'is_superuser', 'is_active')
    ordering = ('email',)
    search_fields = ('email', 'nome', 'sobrenome', 'telefone')
    readonly_fields = ('last_login', 'email_confirmado')
    list_filter = ('is_staff', 'is_active', 'email_confirmado')

    # how fields are displayed when editing an existing user
    fieldsets = (
        ('Login info', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('nome', 'sobrenome', 'telefone', 'email_confirmado')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)})
    )

    # how fields are displayed when creating a new user
    add_fieldsets = (
        ('Register info', {
            'classes': ('wide',),
            'fields': ('email', 'nome', 'sobrenome', 'telefone', 'password1', 'password2'),
        }),
    )
