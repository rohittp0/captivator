from django.http import HttpResponseRedirect
from django.shortcuts import render


def index(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect('admin/login/?next=/')

    return render(request, 'home/index.html')

