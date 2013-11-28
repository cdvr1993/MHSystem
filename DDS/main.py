# -*- coding: utf-8 -*-

__author__ = 'cristian'
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from utils import DecodeKey, DecodeData as DD, ShowError
from DDS.models import TipoUsuario as Type

"""
    Funciones generales
"""

def actionLogin(request):
    from utils import Create
    #Create()
    if request.method == 'GET':
        return render_to_response('login.html')
    else:
        d = request.POST
        try:
            user = auth.authenticate(username=d['username'], password=d['password'])
            if user is None:
                try:
                    User.objects.get(username=d['username'])
                except User.DoesNotExist:
                    return ShowError('No existe el usuario')
                try:
                    User.objects.get(password=d['password'])
                except User.DoesNotExist:
                    return ShowError('Contraseña incorrecta')
            else:
                auth.login(request=request, user=user)
                tipo = GetTypeOfUser(user=user)
                print user.is_active
                if tipo == 1:
                     return HttpResponseRedirect('/administrator/')
                elif tipo == 2:
                    return HttpResponseRedirect('/doctor/')
                elif tipo == 3:
                    return HttpResponseRedirect('/patient/')
                else:
                    return ShowError('No existe todavía ese tipo de usuario')
        except Exception, e:
            return ShowError(e.__str__())

@login_required
def actionLogout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

'''
    Funciones que servirán de apoyo
'''

def GetTypeOfUser(user):
    try:
        return Type.objects.get(id_user=user).tipo
    except Exception:
        raise Exception('No existe')

"""
    Todas las funciones que manejarán la encriptación de los datos que sea necesario encriptar
"""

def SaveKey(request):
    if request.is_ajax() and request.method == 'POST':
        key = request.POST["key"]
        enc = request.POST["enc"]
        global keyFile
        keyFile = str(DecodeKey(key, enc))
        html = "true"
    else:
        html = "false"
    return HttpResponse(html)


def DecodeData(request):
    if request.is_ajax() and request.method == 'POST':
        html = DD(request.POST["Name"])
        acentos = request.POST["Til"]
        acentos = acentos.split(',')
        i = 0
        salida = ""
        for c in html:
            if c == '?':
                salida += acentos[i]
                i += 1
            else:
                salida += c
        return HttpResponse(salida)
