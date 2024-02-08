from django.http import HttpResponseRedirect
from django.shortcuts import render

from home.models import Device


def try_unblock(ip):
    if not ip:
        return "No IP address found"

    device = Device.get_by_ip(ip)

    if not device:
        return "Device discovery failed"

    if device.disabled:
        return "Device is disabled by admin"

    if device.unblock():
        return "Happy browsing!"

    return "Failed to unblock device"


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('admin/login/?next=/')

    ip = request.META.get('REMOTE_ADDR')
    msg = try_unblock(ip)

    return render(request, 'home/index.html', {'msg': msg})
