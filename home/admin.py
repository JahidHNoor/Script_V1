from django.contrib import admin
from django.contrib.auth import get_user_model
from home.models import *

# Register your models here.

User = get_user_model()

def has_superuser_permission(request):
    return request.user.is_active and request.user.is_superuser

# Only superuser can access root admin site (default)
admin.site.has_permission = has_superuser_permission

class SettingAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Profile)
admin.site.register(Setting, SettingAdmin)
admin.site.register(Available_country)

