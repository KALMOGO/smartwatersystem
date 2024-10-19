from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ("id", "first_name", "last_name", "email", "photo", "tel", 'is_active', 'is_staff', 'last_login')
    
    # Define custom fieldsets
    custom_fieldsets = (
        (None, {'fields': ("first_name", "last_name", "email", "photo", "tel", 'is_active', 'is_staff', 'last_login')}),
    )
    
    # Extract and modify the default fieldsets from BaseUserAdmin
    base_fieldsets = list(BaseUserAdmin.fieldsets)
    # Remove fields from base_fieldsets that are already in custom_fieldsets
    for i, (title, fieldset) in enumerate(base_fieldsets):
        fieldset_fields = fieldset['fields']
        if isinstance(fieldset_fields, tuple):
            base_fieldsets[i] = (title, {'fields': tuple(field for field in fieldset_fields if field not in ["first_name", "last_name", "email", 'is_active', 'is_staff', 'last_login', 'photo', 'tel'])})

    # Combine custom_fieldsets with the modified base_fieldsets
    fieldsets = custom_fieldsets + tuple(base_fieldsets)

    add_fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'password1', 'password2')}),
    )
    ordering = ('first_name',)
    search_fields = ['first_name', 'last_name', 'email']  # Define fields for search

# Register your custom UserAdmin
admin.site.register(User, UserAdmin)
