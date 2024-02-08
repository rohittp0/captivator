from django.contrib import admin

from home.models import Device, ActivityLog


# Register your models here.
@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip', 'mac', 'last_seen', 'user', 'blocked')
    list_filter = ('user', 'blocked')
    search_fields = ('name', 'ip', 'mac')
    ordering = ('user', 'name')
    readonly_fields = ('last_seen', 'blocked', 'online')

    actions = ['block', 'unblock']

    @staticmethod
    def block(request, queryset):
        for device in queryset:
            device.block()
            device.disabled = True
            ActivityLog.objects.create(device=device, action="Disabled by admin")
            device.save()

    block.short_description = "Block selected devices"

    @staticmethod
    def unblock(request, queryset):
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
