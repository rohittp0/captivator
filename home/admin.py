from django.contrib import admin

from home.models import Device, ActivityLog


# Register your models here.
@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip', 'mac', 'last_seen', 'user', 'blocked')
    list_filter = ('user', 'blocked')
    search_fields = ('name', 'ip', 'mac')
    ordering = ('user', 'name')
    readonly_fields = ('last_seen', 'blocked', 'online', 'disabled')

    actions = ['block', 'unblock']

    @admin.action(description="Block")
    def block(self, request, queryset):
        for device in queryset:
            device.block()
            device.disabled = True
            ActivityLog.objects.create(device=device, action="Disabled by admin")
            device.save()

    @admin.action(description="Unblock")
    def unblock(self, request, queryset):
        for device in queryset:
            device.disabled = False
            device.save()
            ActivityLog.objects.create(device=device, action="Enabled by admin")
            device.unblock()


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp', 'device', 'action')
    list_filter = ('device', 'action')
    search_fields = ('device', 'action')
    ordering = ('-timestamp',)
