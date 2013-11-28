# -*- coding: utf-8 -*-
__author__ = 'cristian'

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from HAdmin.models import Administrador, getCount as getCountAdmin
from forms import AdministradorForm, UserForm, Doctorform
from HDoctors.models import Doctor, Permisos, getCount as getCountDoctor
from HPatients.models import Pacientes, getCount as getCountPatient
from DDS.models import TipoUsuario as Type
from DDS.utils import ShowError, isAdmin, CreateUser, RenderWithUser
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.template import RequestContext

#   Funciones que manejará únicamente el administrador del sistema
@login_required
@isAdmin
def HomeAdministrador(request):
    from DDS.models import Hospital
    hosp = Hospital.objects.all()[0]
    dict = {'Hospital': hosp}
    return RenderWithUser(request=request, template='Administrador/index.html', dict=dict).getRendered()

@login_required
@isAdmin
def ListaDeUsuarios(request):
    # Función de página de inicio del administrador
    listAdmin = ListaUsers(page=0, type=1).getLista()
    lstBtnAdmin = getBtn(getCountAdmin())
    print lstBtnAdmin
    d = {'Administradores' : listAdmin, 'lstBtnAdmin' : lstBtnAdmin}
    listDoctor = ListaUsers(page=0, type=2).getLista()
    lstBtnDoctor = getBtn(getCountDoctor())
    d.update({'Doctores' : listDoctor, 'lstBtnDoctor' : lstBtnDoctor})
    return RenderWithUser(request=request, template="Administrador/ListaDeUsuarios.html", dict=d).getRendered()

@login_required
@isAdmin
def RegisterAdmin(request):
    # Función de registro de Administradores
    if request.method == 'GET':
        form = AdministradorForm
        user_form = UserForm
        #   Regresamos el formulario sin datos iniciales
        return RenderWithUser(template='Administrador/RegistrarAdmin.html',request=request, dict={"form": form, "user_form": user_form}).getRendered()
    else:
        uForm = UserForm(request.POST)
        aForm = AdministradorForm(request.POST)
        if uForm.is_valid() and aForm.is_valid():
            if DBRegisterAdmin(uForm, aForm):
                #   Devolvemos True para avisar que si se registro el Administrador.
                return HttpResponse('True')
            else:
                return HttpResponse('Error interno')
        #   Regresamos el formulario con los datos obtenidos del POST, solo en caso de error, para que se muestren
        return RenderWithUser(template='Administrador/RegistrarAdmin.html', request=request, dict={"form": aForm, "user_form": uForm}).getRendered()

def DBRegisterAdmin(uForm, aForm):
    try:
        with transaction.commit_on_success():
            user = CreateUser(uForm.cleaned_data)
            d = aForm.cleaned_data
            d.update({'user' : user})
            Administrador().saveWithParams(d)
            return True
    except Exception, e:
        print e
        return False

@login_required
@isAdmin
def RegistrarDoctor(request):
    from forms import PermissionForm
    if request.is_ajax() and request.method == 'POST':
        userForm = UserForm(request.POST)
        dctForm = Doctorform(request.POST)
        perForm = PermissionForm(request.POST)
        if userForm.is_valid() and dctForm.is_valid() and perForm.is_valid():
            if DBRegistrarDoctor(userForm.cleaned_data, dctForm.cleaned_data.copy(), perForm):
                return HttpResponse("True")
            else:
                return HttpResponse("Error interno")
    else:
        userForm = UserForm
        dctForm = Doctorform
        perForm = PermissionForm
    return RenderWithUser(request=request, template='Administrador/RegistrarDoctor.html',
                          dict={'uForm' : userForm, 'dForm' : dctForm, 'pForm' : perForm}).getRendered()

def DBRegistrarDoctor(uForm, d, pForm):
    try:
        with transaction.commit_on_success():
            user = CreateUser(uForm)
            d.update(pForm.cleaned_data)
            d.update({'user' : user})
            dct = Doctor().saveWithParams(d)
            return True
    except Exception, e:
        print e
        return  False


def GeneralListado(request, tipo, filter = None):
    d = request.GET
    page = d.get('page', 0)
    page = int(page) - 1
    nombre = d.get('nombre', '')
    if page == -1:
        return HttpResponse('Faltan argumentos')
    if len(nombre) <= 0:
        lst = ListaUsers(page=page, type=tipo, filtrado=filter).getLista()
    else:
        lstAdmin = ListaUsers(page=page, nombre=nombre, type=tipo, filtrado=filter)
        lstAdmin.getLista()
        lst = lstAdmin.getListaWhileSearching()
    s = {}
    if lst is not None:
        s = {'Administradores' : lst}
    return  lst

def GeneralPaginadorRefresh(tipo, filtrado = None):
    if tipo == 1:
        count = getBtn(getCountAdmin())
        name = 'lstBtnAdmin'
        template = 'Administrador/_adminPaginator.html'
    elif tipo == 2:
        count = getBtn(getCountDoctor())
        name = 'lstBtnDoctor'
        template = "Administrador/DoctorPaginator.html"
    elif tipo == 3:
        count = getBtn(getCountPatient(filtrado=filtrado))
        if filtrado is None:
            name = 'lstBtnPatient'
            template = 'Doctor/PatientPaginator.html'
        else:
            name = 'lstBtnMyPatient'
            template = 'Doctor/MyPatientPaginator.html'
    lstBtn = count
    d = {name : lstBtn}
    return render_to_response(template, d)

def GeneralPaginadorByName(nombre, tipo, filtrado = None):
    lstUser = ListaUsers(page=0, nombre=nombre, type=tipo, filtrado=filtrado)
    lst = lstUser.getLista()
    lstBtnAdmin = getBtn(len(lst))
    lst = lstUser.getListaWhileSearching()
    if lst is not None:
        if tipo == 1:
            templateHigh = 'Administrador/_administradores.html'
            templateLow = 'Administrador/_adminPaginator.html'
            nameList = 'Administradores'
            nameBtn = 'lstBtnAdmin'
        elif tipo == 2:
            templateHigh = 'Administrador/_usuarios.html'
            templateLow = 'Administrador/DoctorPaginator.html'
            nameList = 'Doctores'
            nameBtn = 'lstBtnDoctor'
        elif tipo == 3:
            if filtrado is None:
                templateHigh = 'Doctor/ListaGralPacientes.html'
                templateLow = 'Doctor/PatientPaginator.html'
                nameList = 'Pacientes'
                nameBtn = 'lstBtnPatient'
            else:
                templateHigh = 'Doctor/ListaDePacientes.html'
                templateLow = 'Doctor/MyPatientPaginator.html'
                nameList = 'MyPacientes'
                nameBtn = 'lstBtnMyPatient'
        html = render_to_response(templateHigh, {nameList : lst}).content
        html += render_to_response(templateLow, {nameBtn : lstBtnAdmin}).content
        return HttpResponse(html)

@login_required
@isAdmin
def ListadoDeAdministradores(request):
    # Función que obtendra la lista de administradores, según los parámetros
    s = {}
    lst = GeneralListado(request, 1)
    if lst is not None:
        s = {'Administradores' : lst}
    return render_to_response('Administrador/_administradores.html', s, context_instance=RequestContext(request))

@login_required
@isAdmin
def AdminPaginador(request):
    ''' En caso de que sea la búsqueda por nombre '''
    nombre = request.GET.get('nombre', None)
    if nombre is None:
        return GeneralPaginadorRefresh(1)
    else:
        return GeneralPaginadorByName(nombre, 1)

@login_required
@isAdmin
def ListadoDeDoctores(request):
    s = {}
    lst = GeneralListado(request, 2)
    if lst is not None:
        s = {'Doctores' : lst}
    return render_to_response('Administrador/_usuarios.html', s, context_instance=RequestContext(request))

@login_required
@isAdmin
def DoctorPaginador(request):
    nombre = request.GET.get('nombre', None)
    if nombre is None:
        return GeneralPaginadorRefresh(2)
    else:
        return GeneralPaginadorByName(nombre, 2)

def getBtn(Count):
    lstBtn = []
    i = ListaUsers.limite
    while i < Count:
        lstBtn.append(str(i / ListaUsers.limite + 1))
        i += ListaUsers.limite
    return lstBtn

@login_required
@isAdmin
def DeleteUser(request):
    if request.is_ajax():
        d = request.POST
        idUser = d['ID']
        tipo = int(d['Tipo'])
        if tipo != 1 and tipo != 2:
            # Solo puede dar de baja Administradores y doctores
            raise PermissionDenied
        from DDS.utils import DeleteUser as DU
        return DU(tipo, idUser)
    raise PermissionDenied

@login_required
@isAdmin
def EditUser(request):
    from DDS.utils import EditAnyUser
    if request.method == 'GET':
        id = request.GET['id']
        tipo = int(request.GET['tipo'])
    elif request.is_ajax():
        id = request.POST['id']
        tipo = int(request.POST['tipo'])
    if tipo != 1 and tipo != 2:
        # Solo puede actualizar Administradores y doctores
        raise PermissionDenied
    return EditAnyUser(request, id, tipo)

class ListaUsers():
    ''' Clase que manejará la lista de Administradores '''
    limite = 3
    def __init__(self, page = -1, nombre = None, type = None, filtrado = None):
        self.page = int(page)
        self.nombre = nombre
        self.lstUsers = None
        #Se usará filter únicamente para el doctor para determinar si es la lista completa o nomás sus pacientes
        if type == 1:
            self.lstUsers = Administrador.objects.filter(id_user__is_active=True)
        elif type == 2:
            self.lstUsers = Doctor.objects.filter(id_user__is_active=True)
        elif type ==3:
            if filtrado is None:
                self.lstUsers = Pacientes.objects.filter(id_user__is_active=True)
            else:
                self.lstUsers = Pacientes.objects.filter(id_user__is_active=True).filter(id_doctor=filtrado)

    def getLista(self):
        if self.page == -1 and self.nombre is None:
            return None
        if self.nombre is None:
            if self.page != 0:
                inicio = self.page * ListaUsers.limite
            else:
                inicio = 0
            admin = self.lstUsers[ inicio : inicio + ListaUsers.limite]
            return admin
        else:
            lst = self.lstUsers
            self.oLst = []
            for admin in lst:
                if admin.iContains(self.nombre):
                    self.oLst.append(admin)
            return self.oLst

    def getListaWhileSearching(self):
         if self.page != 0:
            inicio = self.page * ListaUsers.limite
         else:
            inicio = 0
         return self.oLst[ inicio : inicio + ListaUsers.limite]