__author__ = 'cristian'

# Archivo general de pruebas

from django.http import HttpResponse
from django.contrib.auth.models import User

def DelUser(request):
    if request.method == 'GET':
        try:
            username = request.GET['username']
            user = User.objects.get(username=username)
            user.delete()
            html = 'Ok'
        except Exception, e:
            html = e.message
    return HttpResponse(html)

def activateUser(request):
    user = User.objects.get(pk=request.GET['id'])
    user.is_active = True
    user.save()
    user = User.objects.get(pk=user.id)
    if user.is_active:
        return HttpResponse('Se activo con exito')
    else:
        return HttpResponse('Ocurrio un error')

def NotAuthorized(request):
    return HttpResponse(str(request.GET.get('error','')).replace('_',' '))