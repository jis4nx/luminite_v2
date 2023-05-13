from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from .forms import Luminite_UserCreationForm, Luminite_UserChangeForm
from django.contrib.auth import get_user_model

class LuminiteAdmin(UserAdmin):
    add_form = Luminite_UserCreationForm
    form = Luminite_UserChangeForm

    model = get_user_model()

    list_display = ('email', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')


    fieldsets = (
        (None, {'fields':('email', 'password')}),
        ('Permissions', {'fields' : ('is_staff', 'is_superuser', 
                                     'is_active', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
            (None, {'fields': ('email', 'type', 'password', 'password2', 'is_staff', 'is_active')}),
    )

    search_fields = ('email', )
    ordering = ('email',)

admin.site.register(User, LuminiteAdmin)
