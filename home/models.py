import json
from subprocess import run

from django.db import models


# Create your models here.

class Device(models.Model):
    name = models.CharField(max_length=100)
    ip = models.GenericIPAddressField()
    mac = models.CharField(max_length=17)
    last_seen = models.DateTimeField(auto_now=True)

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    blocked = models.BooleanField(default=False)
    online = models.BooleanField(default=True)
    disabled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.name}"

    class Meta:
        ordering = ['user', 'name']
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'

    def block(self):
        data = run(f"wallu block {self.mac}", capture_output=True, shell=True)
        if data.returncode == 0:
            self.blocked = True
            self.save()
            ActivityLog.objects.create(device=self, action="Blocked")

            return True

        ActivityLog.objects.create(device=self, action=f"Failed to block: {data.stderr}")

        return False

    def unblock(self):
        if self.disabled:
            return False

        data = run(f"wallu allow {self.mac}", capture_output=True, shell=True)
        if data.returncode == 0:
            self.blocked = False
            self.save()
            ActivityLog.objects.create(device=self, action="Unblocked")

            return True

        ActivityLog.objects.create(device=self, action=f"Failed to unblock: {data.stderr}")

        return False

    def get_by_ip(ip):
        data = run(f"wallu json {ip}", capture_output=True, shell=True)
        if data.returncode == 0:
            data = json.loads(data.stdout.decode())
            device, created = Device.objects.get_or_create(mac=data['mac'])
            device.name = data['name'] or device.name
            device.ip = ip

            ActivityLog.objects.create(device=device, action=f"Discovered by IP: {ip}")

            return device

        return None


class ActivityLog(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    action = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.device} {self.action} at {self.timestamp}"

    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Activity Log'
        verbose_name_plural = 'Activity Logs'
