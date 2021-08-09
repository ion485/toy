from django.contrib import admin

from .models import User

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'name', 'date_at', 'last_login', 'is_superuser', 'is_staff')
    list_display_links = ('id', 'email')
    exclude = ('password',)

    def date_at(self, obj):
        return obj.date.strftime("%Y-%m-%d")

    def last_login(self, obj):
        if not obj.last_login:
            return ''
        return obj.last_login.strftime("%Y-%m-%d %H:%M")

    date_at.admin_order_field = '-date'
    date_at.short_description = '일자'
    last_login.admin_order_field = 'last_login'
    last_login.short_description = '마지막 로그인'