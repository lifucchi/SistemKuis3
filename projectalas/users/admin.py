from django.contrib import admin

# Register your models here.
# Register your models here.
from users.forms import UserCreationForm, UserChangeForm
from users.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('username', 'first_name','last_name', 'email', 'is_active')
    list_filter = ('username', 'first_name','last_name', 'email', 'is_active')
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name','username', 'email','classes','sekolah' ,'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')})
    )
    search_fields = ('username',)
    ordering = ('username',)


admin.site.register(User, UserAdmin)
from django.contrib import admin
# Register your models here.
