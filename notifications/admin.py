from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "description", "read")
    list_filter = ("read",)
    search_fields = ("user__username", "description")
    readonly_fields = ("user", "description", "read")
