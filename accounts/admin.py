from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUerCreationForm, CustomUserChangeForm
from .models import CustomUser
# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = CustomUerCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'age', 'is_staff',]
    
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields':('age',)}),
        )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'Fields': ('age',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)