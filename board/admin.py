from django.contrib import admin

from .models import para
# Register your models here.

@admin.register(para)
class paraAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'date_created')
    list_display_links = ('id', 'title')

    def date_created(self, obj):
        return obj.date.strftime("%Y-%m-%d")

    date_created.admin_order_field = "date"
    date_created.short_description = '일자'

# admin.site.register(para)