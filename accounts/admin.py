from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
# from django.contrib.auth import get_user_model
from django.utils.html import format_html

from .models import Account, UserProfile
# Register your models here.

class AccountAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email',  'password')}),
        (_('Personal info'), {'fields': ('first_name', 'mobile', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_admin', 'is_verified',
                                       )}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ( 'first_name', 'last_name', 'email', 'mobile', 'password1', 'password2'),
        }),
    )
    list_display = ( 'email','first_name', 'last_name', 'mobile', 'is_active', 'date_joined', 'last_login')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    list_display_links = ('email', 'first_name', 'last_name')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-radius: 50%;">'.format(object.profile_picture.url))
    
    thumbnail.short_description = 'profile_picture'
    list_display=('thumbnail', 'user' )


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Account, AccountAdmin)