from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Профиль'
    fk_name = 'user'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'is_staff', 'get_title'
    )

    def get_title(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.title
        return ''
    get_title.short_description = 'Специализация'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.site_header = 'StudentHub — Админ-панель'
admin.site.site_title = 'StudentHub — Админ-панель'
admin.site.index_title = 'Управление платформой'
