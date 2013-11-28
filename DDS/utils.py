# -*- coding: utf-8 -*-
__author__ = 'cristian'
import subprocess
import sys
import psycopg2 as psql
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.exceptions import PermissionDenied
from HAdmin.models import Administrador
from models import TipoUsuario as Type, Hospital
from HDoctors.models import Doctor
from HPatients.models import Pacientes
from django.contrib.auth.models import User

def Create():
    CreateFirstAdmin({
    'username' : u'cristian',
    'password' : u'david',
    'email' : u'cdvr1993@gmail.com',
    'name' : u'cristian',
    'apaterno' : u'velázquez',
    'amaterno' : u'ramírez',
    'puesto' : u'administrador'
    })
    CreateHospitalInfo({
        'razon' : u'Hospital Santa Margarita S.A. de C.V.',
        'rfc' : u'HSM9312678EW',
        'numero' : u'1345',
        'calle' : u'Santa Margarita',
        'colonia' : u'Centro',
        'municipio' : u'Guadalajara',
        'estado' : u'Jalisco'
    })

def CreateFirstAdmin(dict = None):
    create = False
    if Administrador.objects.all().count() == 0:
        create = True
    if dict is None:
        raise Exception('First username dictionary is not defined')
    # Crearemos el primer usuario
    from HAdmin.forms import EmailForm, AdministradorForm
    uForm = EmailForm(dict)
    aForm = AdministradorForm(dict)
    if aForm.is_valid() and uForm.is_valid():
        if create:
            from HAdmin.Administrador import DBRegisterAdmin
            DBRegisterAdmin(uForm, aForm)
        else:
            user = User.objects.get(pk=1)
            user.username = dict['username']
            from django.contrib.auth.hashers import make_password
            user.password = make_password(dict['password'])
            user.email = dict['email']
            user.is_active = True
            user.save()
            adm = Administrador.objects.get(id_user=user.id)
            adm.inserDict(dict)

def CreateHospitalInfo(dict = None):
    create = False
    if Hospital.objects.all() > 0:
        create = True
    if dict is None:
        raise Exception('Hospital dictionary is not defined')
    # También crearemos la información del Hospital
    if create:
        h = Hospital()
    else:
        h = Hospital.objects.get(pk=1)
    h.razon = dict['razon']
    h.rfc = dict['rfc']
    h.numero = dict['numero']
    h.calle = dict['calle']
    h.colonia = dict['colonia']
    h.municipio = dict['municipio']
    h.estado = dict['estado']
    h.save()

def CreateUser(dict = None):
    if dict is None:
        return None
    return User.objects.create_user(username=dict['username'], password=dict['password'], email=dict['email'])

def EditAnyUser(request, id, tipo):
    # Se dividió la función en GET y en POST por el tamaño de lo que se realizaba dentro de los ifs
    if request.method == 'GET':
        return EditAnyUserGet(request, id, tipo)
    elif request.is_ajax():
        return EditAnyUserPost(request, id, tipo)


def EditAnyUserGet(request, id, tipo):
    # Función que presenta el form con los datos del usuario seleccionado para ser modificado.
    from HDoctors.models import Permisos
    from HAdmin.forms import AdministradorForm, EmailForm, Doctorform, PermissionForm
    dict = {'Edit' : True, 'EditID' : id, 'TipoInt' : tipo}
    user = User.objects.filter(pk=id).values()[0]
    user_form = EmailForm(user)
    # Se comprueba que él que lo esta accediendo tiene los permisos necesarios, ya que solo el admin puede modificar tipo 1 y 2
    if tipo == 1:
        form = AdministradorForm(Administrador.objects.filter(id_user=id).values()[0])
        dict.update({'form' : form, 'user_form' : user_form})
        tmpl = 'Administrador/RegistrarAdmin.html'
    elif tipo == 2:
        doc = Doctor.objects.filter(id_user=id)
        form = Doctorform(doc.values()[0])
        pForm = PermissionForm(Permisos.objects.filter(id_user=doc[0].id).values()[0])
        dict.update({'dForm' : form, 'uForm' : user_form, 'pForm' : pForm})
        tmpl = 'Administrador/RegistrarDoctor.html'
    elif tipo == 3:
        from HDoctors.forms import PatientForm
        form = PatientForm(Pacientes.objects.filter(id_user=id).values()[0])
        dict.update({'uForm' : user_form, 'pForm' : form})
        tmpl = 'Doctor/registrarPaciente.html'
    return RenderWithUser(template=tmpl, request=request, dict=dict).getRendered()

def EditAnyUserPost(request, id, tipo):
    # Función que solocita la actualización de los cambios introducidos por el usuario.
    from HAdmin.forms import AdministradorForm, EmailForm, Doctorform, PermissionForm
    uForm = EmailForm(request.POST)
    Form = None
    response = None
    dict = {}
    permForm = None
    # Se vuelve a comprobar que sea el admin el que esta tratando de modificar tipo 1 y tipo 2
    if tipo == 1:
        Form = AdministradorForm(request.POST)
        tmpl = 'Administrador/RegistrarAdmin.html'
        uSForm = "user_form"
        pForm = "form"
        response = 'True - Admin'
    elif tipo == 2:
        Form = Doctorform(request.POST)
        permForm = PermissionForm(request.POST)
        permFormValid = permForm.is_valid()
        tmpl = "Administrador/RegistrarDoctor.html"
        uSForm = "uForm"
        pForm = "dForm"
        # Aquí actualizamos el diccionario únicamente con este form ya que es propio del doctor
        dict.update({'pForm' : permForm})
        response = 'True - Admin'
    elif tipo == 3:
        from HDoctors.forms import PatientForm
        Form = PatientForm(request.POST)
        tmpl = "Doctor/registrarPaciente.html"
        uSForm = "uForm"
        pForm = "pForm"
        response = 'True - Doctor'
    # Validamos los dos primeros diccionarios para comprobar solo una vez
    uFormValid = uForm.is_valid()
    FormValid = Form.is_valid()
    # Primero validamos que exista el Form, posteriormente comprobamos que los forms que comparten los tres tipos de usuario
    # sea válido. En lo que sigue se comprueba que si el form de permisos existe entonces es modificación de un doctor y tmb se
    # debe de comprobar que los datos que contiene sea válido.
    if Form is not None and \
            ((uFormValid and FormValid) or
                 (uFormValid and FormValid and permForm is not None and permFormValid)):
        # Primero actualizamos al usuario
        from DDS.utils import UpdateUser
        UpdateUser(id=id, dict=uForm.cleaned_data)
        # Después nos ponemos a actualizar al tipo de usuario que corresponda.
        if tipo == 1:
            Administrador().Update(id=id, dict=Form.cleaned_data)
        elif tipo == 2:
            Doctor().Update(id=id, dict=Form.cleaned_data)
            from HDoctors.models import Permisos
            Permisos().Update(id=id, dict=permForm.cleaned_data)
        elif tipo == 3:
            Pacientes().Update(id=id, dict=Form.cleaned_data)
        return HttpResponse(response)
    try:
        # Usamos un try para marcarlo como permiso denegado
        # A continuación solo actualizamos los que corresponde a los tres tipos de usuario.
        dict.update({pForm : Form, uSForm: uForm, 'Edit' : True, 'EditID' : id, 'TipoInt' : tipo})
        return RenderWithUser(template=tmpl, request=request, dict=dict).getRendered()
    except Exception:
        raise PermissionDenied

def UpdateUser(id = -1, dict = None):
    # Función que actualiza la información del usuario, que en nuestro caso solo es el e-mail
    if id == -1 or dict is None:
        return False
    from django.contrib.auth.models import User
    user = User.objects.get(pk=id)
    user.email = dict.get('email', user.email)
    user.save()

def DeleteUser(tipo = -1, idUser = -1):
    # Función que elimina el usuario dependiendo del tipo, pero el eliminar significa darlo de baja,
    # para que no halla problema con dependencias.
    if tipo == -1 and idUser == -1:
        raise Exception("No se puede eliminar porque no hay parámetros")
    user = None
    if tipo == 1:
        user = Administrador.objects.get(id_user=idUser)
    elif tipo == 2:
        user = Doctor.objects.get(id_user=idUser)
    elif tipo == 3:
        user = Pacientes.objects.get(id_user=idUser)
    if user is None:
        raise Exception('No tiene los permisos para borrar')
    name = user.name + ' ' + user.apaterno + ' ' + user.amaterno
    user.id_user.is_active = False
    user.id_user.save()
    return HttpResponse(u'Usuario ha sido marcado como inactivo éxitosamente >> "' + name + '"')

def CapitalizeDict(d = None):
    # Función que pone las primeras letras de la palabra de todos los strings que esten en el diccionario
    exc = ('rfc', 'curp', 'matricula')
    # Arriba ponemos las excepciones a cambiar de string.
    if d is None:
        raise Exception('El diccionario no es válido')
    for key in d.iterkeys():
        if type(d[key]) == type(u'') and not exc.__contains__(key):
            d[key] = CapStr(d[key])

def CapStr(string):
    try:
        salida = []
        aux = ''
        for c in string:
            salida.append(c)
        for x in range(0, len(salida)):
            if x == 0:
                salida[x] = salida[x].upper()
            elif salida[x] == ' ':
                salida[x+1] = salida[x+1].upper()
            aux += salida[x]
        return aux
    except Exception:
        return string

def isAdmin(f = None):
    ''' Decorador que comprueba si el usuario es de tipo Admin '''
    def actual_decorator(*args):
        request = args[0]
        # En caso de que no sea Administrador devuelve error
        if Type.objects.get(id_user=request.user).tipo != 1 or not request.user.is_active:
            print request.user.is_active
            raise  PermissionDenied
        # Si si es, devuelve la función original
        return f(*args)
    return actual_decorator

def isDoctor(f = None):
    ''' Decorador que comprueba si el usuario es de tipo Doctor'''
    def actual_decorator(*args):
        request = args[0]
        # En caso de que no sea Doctor devuelve error
        from HDoctors.models import Permisos
        if Type.objects.get(id_user=request.user).tipo != 2 or not request.user.is_active or \
            not Permisos.objects.get(id_user=Doctor.objects.get(id_user=request.user)).acceso:
            raise  PermissionDenied
        # Si si es, devuelve la función original
        return f(*args)
    return actual_decorator

def FullPatientView(f = None):
    ''' Decorador que comprueba si el doctor tiene permisos para ver todos los doctores'''
    def actual_decorator(*args):
        request = args[0]
        # En caso de que no sea Doctor devuelve error
        from HDoctors.models import Permisos
        if not Permisos.objects.get(id_user=Doctor.objects.get(id_user=request.user)).full_view:
            raise  PermissionDenied
        # Si si es, devuelve la función original
        return f(*args)
    return actual_decorator

def isPatient(f = None):
    ''' Decorador que comprueba si el usuario es de tipo Doctor'''
    def actual_decorator(*args):
        request = args[0]
        # En caso de que no sea Doctor devuelve error
        from HDoctors.models import Permisos
        if Type.objects.get(id_user=request.user).tipo != 3 or not request.user.is_active:
            raise  PermissionDenied
        # Si si es, devuelve la función original
        return f(*args)
    return actual_decorator

def GetDateRange(list, range):
    if range[0] == '':
        range[0] = list.objects.order_by('fech')[0].fech
    if range[1] == '':
        from datetime import datetime as dt
        range[1] = dt.today()

def DecodeKey(key, enc):
    decrypted = ComandoConsola('seed /home/cristian/Documentos/main.js "' + str(key) + '" "' + str(enc) + '"')
    con = psql.connect(database='Prueba', user='postgres', password='kiwi')
    cur = con.cursor()
    cur.execute('SELECT * FROM TRANSACCION WHERE IDUSUA=0')
    if cur.fetchone() is None:
        cur.execute("INSERT INTO TRANSACCION VALUES(0,'" + str(decrypted) + "')")
    else:
        cur.execute("UPDATE TRANSACCION SET KEY='" + str(decrypted) + "' WHERE IDUSUA=0")
    con.commit()
    return decrypted


def DecodeData(data):
    con = psql.connect(database='Prueba', user='postgres', password='kiwi')
    cur = con.cursor()
    cur.execute('SELECT * FROM TRANSACCION WHERE IDUSUA=0')
    key = cur.fetchone()
    key = key[1]
    decrypted = ComandoConsola('seed /home/cristian/Documentos/main.js "' + str(key) + '" "' + str(data) + '"')
    return decrypted

def ComandoConsola(comando):
    comando = comando.replace('\n', '')
    proceso = subprocess.Popen(comando, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    salida = ""
    while True:
        next_line = proceso.stdout.readline()
        salida += next_line
        if next_line == '' and proceso.poll() != None:
            break
        sys.stdout.write(next_line)
        sys.stdout.flush()
    print salida
    return salida

def ShowError(exception):
    return HttpResponse('Ocurrio un error:<br>' + exception)

class RenderWithUser:
    # Clase que maneja el render_to_response para todas las páginas para agregar el nombre y tipo de usuario en todos
    # los renderizados de las páginas, excepto en las de logueo.
    def __init__(self, request = None, template = None, dict = None):
        self.request = request
        self.__user = request.user
        self.__template = template
        self.__dict = dict

    def getRendered(self):
        if self.__user is None:
            raise PermissionDenied
        tipo = Type.objects.get(id_user=self.__user).tipo
        resDict = {}
        if tipo == 1:
            user = Administrador.objects.get(id_user=self.__user)
            tipoStr = "Administrador"
        elif tipo == 2:
            user = Doctor.objects.get(id_user=self.__user)
            tipoStr = 'Doctor'
        elif tipo == 3:
            user = Pacientes.objects.get(id_user=self.__user)
            tipoStr = 'Paciente'
        else:
            raise Exception('No existe ese tipo de usuario')
        resDict = {"Usuario" : user, "Tipo" : tipoStr}
        if self.__dict is None:
            self.__dict = resDict
        else:
            self.__dict.update(resDict)
        from django.template import RequestContext
        return render_to_response(self.__template, self.__dict, context_instance=RequestContext(self.request))
