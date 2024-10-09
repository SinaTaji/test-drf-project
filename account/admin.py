from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import UserCreationForm, UserChangeForm


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'phone_number', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('is_active',)

    fieldsets = [
        (None, {'fields': ('username', 'phone_number')}),
    ]
    add_fieldsets = [
        (None, {'fields': ('username', 'phone_number', 'password', 'password2')}),
    ]
    search_fields = ('phone_number',)
    ordering = ('username',)
    filter_horizontal = []
