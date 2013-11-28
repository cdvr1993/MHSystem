__author__ = 'cristian'
# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from DDS.utils import RenderWithUser, isDoctor, CreateUser, FullPatientView
from HAdmin.forms import UserForm
from forms import PatientForm
from models import Doctor, Permisos
from HPatients.models import Pacientes, getCount
from django.core.exceptions import PermissionDenied
from django.db import transaction
from HPatients.models import Pacientes,Medicamento,NombreM,Preescripciones,Indicaciones,Diagnosticos

@login_required
@isDoctor
def HomeDoctor(request):
    doc = Doctor.objects.get(id_user=request.user)
    dict = {'dForm' : doc}
    dict.update({'uForm': request.user})
    from HAdmin.Administrador import ListaUsers, getBtn
    listDoctor = ListaUsers(page=0, type=3, filtrado=doc).getLista()
    # A continuación obtenemos únicamente los pacientes de este doctor
    lstBtnDoctor = getBtn(getCount(filtrado=doc))
    dict.update({'MyPacientes' : listDoctor, 'lstBtnMyPatient' : lstBtnDoctor})
    # A continuación obtenemos todos los pacientes solo si tiene el permiso para verlos
    if Permisos.objects.get(id_user=doc).full_view:
        lstBtnDoctor = getBtn(getCount())
        listDoctor = ListaUsers(page=0, type=3).getLista()
        dict.update({'Pacientes' : listDoctor, 'lstBtnPatient' : lstBtnDoctor, 'GralList' : True})
    return RenderWithUser(request=request, template='Doctor/index.html', dict=dict).getRendered()

@login_required
@isDoctor
def RegisterPatient(request):
    if request.is_ajax() and request.method=='POST':
        userForm=UserForm(request.POST)
        pteForm=PatientForm(request.POST)
        if userForm.is_valid() and pteForm.is_valid():
            if DBRegisterPatient(request.user, userForm.cleaned_data, pteForm.cleaned_data.copy()):
                from DDS.models import Hospital
                hopsital = Hospital.objects.get(pk=1)
                mensaje = request.POST.get('name',"")+" "+request.POST.get('apaterno',"")+" "+request.POST.get('amaterno',"")+", bienvenido a "+hopsital.razon+"\n\nUsuario: "+request.POST.get('username',"")+"\nContrasena: "+request.POST.get('password',"")
                from django.core.mail import send_mail
                send_mail(subject='Bienvenido a '+hopsital.razon, message=mensaje, from_email="mira0993@gmail.com",
                recipient_list=[userForm.cleaned_data['email']], fail_silently=False)
                return HttpResponse("True")
            return HttpResponse("Error interno")
        else:
            print pteForm.errors
    else:
        userForm = UserForm
        pteForm = PatientForm
    return RenderWithUser(request=request, template='Doctor/registrarPaciente.html',
                          dict={'uForm' : userForm, 'pForm' : pteForm}).getRendered()

def DBRegisterPatient(uDoctor, uForm, paciente):
    try:
        with transaction.commit_on_success():
            user = CreateUser(uForm)
            paciente.update({'user': user})
            from HDoctors.models import Doctor
            paciente.update({'doctor': Doctor.objects.get(id_user=uDoctor)})
            dct = Pacientes().saveWithParams(paciente)
            return True
    except Exception, e:
        print e
        return False

@login_required
@isDoctor
def Diagnostico(request):
    from models import Doctor,Permisos
    from HPatients.forms import DiagnosisForm
    import datetime
    fecha=str(datetime.datetime.now().day)+'/ '+str(datetime.datetime.now().month)+'/ '+str(datetime.datetime.now().year)
    hora= str(datetime.datetime.now().hour)+': '+str(datetime.datetime.now().minute)

    doctor=Doctor.objects.get(id_user=request.user)
    permisos=Permisos.objects.get(id_user=doctor.id)
    lista=[]
    actual=[]
    form = DiagnosisForm
    if request.method=='GET':
        lista = ListaPacientes().obtainSerach(doctor.id,permisos.full_view,request.GET.get('nombre'))
    if request.is_ajax and request.method=='POST':
        print request.POST
        form = DiagnosisForm(request.POST)
        if form.is_valid():
            diagnostico=form.cleaned_data
            idPaciente = int(request.POST.get('IDP'))
            print "El id del paciente es"
            print idPaciente
            diagnostico.update({'doctor':doctor.id})
            diagnostico.update({'paciente':idPaciente})
            diagnostico.update({'presc':None})
            Diagnosticos().saveWithParams(diagnostico)
            return HttpResponse('True')
    print form
    return RenderWithUser(request=request, template="Doctor/Diagnostico.html",dict={"Pacientes":lista,"Current":actual,"DiagnosisForm":form,"Fecha":fecha,"Hora":hora}).getRendered()

@login_required
@isDoctor
def UploadRequest(request):
    lista=[]
    actual=[]
    from models import Doctor,Permisos
    doctor=Doctor.objects.get(id_user=request.user)
    permisos=Permisos.objects.get(id_user=doctor.id)
    dic = {}
    from forms import UploadForm
    if request.method == 'GET':
        uForm = UploadForm
        n = request.GET.get('nombre')
        if n is None:
            lista = ListaPacientes().obtainSerach(doctor.id,permisos.full_view)
        else:
            lista = ListaPacientes().obtainSerach(doctor.id,permisos.full_view,request.GET.get('nombre'))
        dic.update({'Pacientes': lista,'Current':actual})
    else:
        # Se manda llamar al POST
        uForm = UploadForm(request.POST, request.FILES)
        resp = UploadPost(request, uForm, request.POST['id'], request.user)
        if resp != None:
            return resp
    dic.update({'uForm' : uForm})
    return RenderWithUser(request=request, template='Doctor/upload.html', dict=dic).getRendered()

def UploadPost(request, uForm, id, user):
    # No se generó con jQuery porqué había que agregar más plugins
    if uForm.is_valid():
        from DDS.settings import MEDIA_ROOT
        from HPatients.models import Analisis
        from datetime import datetime as dt
        from os.path import exists
        # Variable que manejara el mensaje de éxito
        suc_msg = ''
        d = uForm.cleaned_data.copy()
        patient = Pacientes.objects.get(id_user=id)
        fi = d['file']
        # Buscaremos la extensión del archivo
        ext = '.pdf'
        import os
        dir = MEDIA_ROOT[0] + '/%s' % str(patient.id)
        if not os.path.exists(dir):
            os.makedirs(dir)
        path = '/%s/%s' % (dir, (d['name'] + ext))
        if exists(path):
            path = '%s_1%s' % (path[: -4], ext)
            suc_msg = '%s' % (path[path.rfind('/') + 1 : ])
        f = open(path, 'w')
        f.write(fi.read(fi.size))
        f.close()
        d.update({'id_user' : Doctor.objects.get(id_user=user), 'id_paciente' : patient,
                  'fech_up' : dt.today(), 'tipo' : 'indefinido', 'path' : path })
        Analisis().saveWithParams(d)
        return RenderWithUser(request=request, template='Doctor/upload.html', dict={'uForm' : uForm, 'success': True, 'suc_msg' : suc_msg }).getRendered()

@login_required
@isDoctor
def Historial(request):
    from forms import HistorialSearch
    if request.method == 'GET':
        sForm = HistorialSearch
    return RenderWithUser(request=request, template="Doctor/busquedaDate.html", dict={'sForm' : sForm}).getRendered()

def getHistorialFilter(request):
    # Función que manejará el filtro de la búsqueda de diagnósticos
    d = request.GET
    name = d['name']
    init = d['init']
    final = d['final']
    from DDS.utils import GetDateRange
    rango = [init, final]
    GetDateRange(Diagnosticos, rango)
    from forms import HistorialSearch
    hs = HistorialSearch({ 'name' : name, 'init': rango[0], 'final' : rango[1] })
    if hs.is_valid():
        d = hs.cleaned_data
        doc = Doctor.objects.get(id_user=request.user)
        tmp = Diagnosticos.objects
        if not Permisos.objects.get(id_user=doc).full_view:
            tmp = tmp.filter(id_user=doc)
        tmp = tmp.filter(fech__range=(d['init'], d['final']))
        if name != '':
            # Aquí agregaríamos únicamente los pacientes que coincidan con el filtro por nombre
            diag = []
            for aux in tmp:
                if aux.id_paciente.iContains(name):
                    diag.append(aux)
        return render_to_response("Doctor/Historial.html", { "diagnosticos" : tmp })
    return RenderWithUser(request=request, template="Doctor/busquedaDate.html", dict={'sForm' : hs}).getRendered()

from HAdmin.Administrador import GeneralListado, GeneralPaginadorByName, GeneralPaginadorRefresh, ListaDeUsuarios

@login_required
@isDoctor
def DoctorPaginador(request):
    nombre = request.GET.get('nombre', None)
    if nombre is None:
        return GeneralPaginadorRefresh(3)
    else:
        return GeneralPaginadorByName(nombre, 3)

@login_required
@isDoctor
def ListadoDePacientes(request):
    # Es el listado de los pacientes propios del doctor
    s = {}
    lst = GeneralListado(request, 3, Doctor.objects.get(id_user=request.user))
    if lst is not None:
        s = {'MyPacientes' : lst}
    return render_to_response('Doctor/ListaDePacientes.html', s)

@login_required
@isDoctor
def MyPatientPaginador(request):
    nombre = request.GET.get('nombre', None)
    if nombre is None:
        return GeneralPaginadorRefresh(3, Doctor.objects.get(id_user=request.user))
    else:
        return GeneralPaginadorByName(nombre, 3, Doctor.objects.get(id_user=request.user))

@login_required
@isDoctor
@FullPatientView
def ListadoGralPacientes(request):
     # Es el listado de todos los pacientes
    s = {}
    lst = GeneralListado(request, 3)
    if lst is not None:
        s = {'Pacientes' : lst}
    return render_to_response('Doctor/ListaGralPacientes.html', s)

@login_required
@isDoctor
@FullPatientView
def PatientPaginator(request):
    nombre = request.GET.get('nombre', None)
    if nombre is None:
        return GeneralPaginadorRefresh(3)
    else:
        return GeneralPaginadorByName(nombre, 3)

@login_required
@isDoctor
def EditUser(request):
    from DDS.utils import EditAnyUser
    # Validamos que si es una lista de sus propios pacientes, entonces debe de ser el doctor de ese paciente
    #print Pacientes.objects.get(id_user=request.GET['id']).id_doctor.id
    if request.method == 'GET':
        id = request.GET['id']
        if request.GET.get('doctor', '') != '' and \
                    Pacientes.objects.get(id_user=id).id_doctor != Doctor.objects.get(id_user=request.user):
            raise PermissionDenied
    elif request.is_ajax():
        id = request.POST['id']
    return EditAnyUser(request, id, 3)

@login_required
@isDoctor
def DeleteUser(request):
    from DDS.utils import DeleteUser
    print request.POST['Doctor']
    if request.POST['Doctor'] == 'True' and \
                    Pacientes.objects.get(id_user=request.POST['ID']).id_doctor != Doctor.objects.get(id_user=request.user):
        raise PermissionDenied
    return DeleteUser(3, request.POST['ID'])

@login_required
@isDoctor
def selectionB(request):
    lista=[]
    actual=[]
    from models import Doctor,Permisos
    doctor=Doctor.objects.get(id_user=request.user)
    permisos=Permisos.objects.get(id_user=doctor.id)

    if request.is_ajax() and request.method=='POST':
        idUser = int(request.POST.get('ID'))
        actual = Pacientes.objects.filter(id_user=idUser)
    else:
        n = request.GET.get('nombre')
        if n is None:
            lista = ListaPacientes().obtainSerach(doctor.id,permisos.full_view)
        else:
            lista = ListaPacientes().obtainSerach(doctor.id,permisos.full_view,request.GET.get('nombre'))
            print 'request '+n
    dicc={'Pacientes': lista,'Current':actual}
    return render_to_response("Doctor/busqueda.html",dicc)

@login_required
@isDoctor
def Diagnostico(request):
    from models import Doctor,Permisos
    from HPatients.forms import DiagnosisForm
    import datetime
    fecha=str(datetime.datetime.now().day)+'/ '+str(datetime.datetime.now().month)+'/ '+str(datetime.datetime.now().year)
    hora= str(datetime.datetime.now().hour)+': '+str(datetime.datetime.now().minute)

    doctor=Doctor.objects.get(id_user=request.user)
    permisos=Permisos.objects.get(id_user=doctor.id)
    lista=[]
    actual=[]
    form = DiagnosisForm
    idDiag=0
    if request.method=='GET':
        lista = ListaPacientes().obtainSerach(doctor.id,permisos.full_view,request.GET.get('nombre'))

    if request.is_ajax and request.method=='POST':
        print request.POST
        form = DiagnosisForm(request.POST)
        if form.is_valid():
            diagnostico=form.cleaned_data
            idPaciente = int(request.POST.get('IDP'))
            diagnostico.update({'doctor':doctor.id})
            diagnostico.update({'paciente':idPaciente})
            diagnostico.update({'presc':None})
            from HPatients.models import Diagnosticos
            idDiag=Diagnosticos().saveWithParams(diagnostico)

    return RenderWithUser(request=request, template="Doctor/Diagnostico.html",dict={"Pacientes":lista,"Current":actual,
                "DiagnosisForm":form,"Fecha":fecha,"Hora":hora,"idDiagnostico":idDiag}).getRendered()

class ListaPacientes():
    def __init__(self):
        self.busqueda =  None
        self.newpte=[]

    def obtainSerach(self, idd, view, nombre= None ):
        pte = self.getList(idd,view)
        self.busqueda = nombre
        if self.busqueda is None:
            return pte
        else:
            self.newpte =[]
            for p in pte:
                if p.iContains(self.busqueda):
                    self.newpte.append(p)
            return self.newpte

    def getList(self,idDoctor, full_view):
        if not full_view:
            pte = Pacientes.objects.filter(id_user__is_active=True).filter(id_doctor=idDoctor).order_by("name","apaterno","amaterno")
        else:
            pte = Pacientes.objects.filter(id_user__is_active=True).order_by("name","apaterno","amaterno")
        return pte

@login_required
@isDoctor
def searchMeds(request):
    nom = []
    meds = []
    desc = []
    actual = []

    if request.method == 'POST'and request.is_ajax:
        idNomMed = request.POST.get("IDNom")
        idMed = request.POST.get("IDDes")
        num = request.POST.get("num")
        if idMed != "":
            actual = Medicamento.objects.get(id = idMed)
        if idNomMed != "":
            nom = NombreM.objects.get(id = idNomMed)
        print request.POST
        print actual.descripcion
        print actual.cantidad
        print actual.unidad
        print nom.medicamento
    else:
        meds = ListaMedicinas().getListOfMedicines(med = request.GET.get('search'))
        if request.GET.get('idmed')!="":
            desc = ListaMedicinas().getDescriptions(idmed=request.GET.get('idmed'))
        num = request.GET.get("num")
    dicc = {'CurrentName':nom,'Current':actual, 'Medicinas': meds,'Desc':desc,'num':num}
    return render_to_response("Doctor/medicamentos.html",dicc)

class ListaMedicinas():

    def getListOfMedicines(self, med = None):
        lista = NombreM.objects.filter().order_by("medicamento")
        if med is None:
            return lista

        else:
            filter_lista = []
            search= str(med)
            for m in lista:
                if m.medicamento.__contains__(search.upper()):
                    filter_lista.append(m)
            return filter_lista

    def getDescriptions(self, idmed = None):
        desc = []
        if desc is not None:
            desc = Medicamento.objects.filter(id_Nombre=idmed)
        return desc

@login_required
@isDoctor
def Prescripciones(request):
    import datetime
    Pte=[]
    idPresc=0
    idDiag = 0
    fecha=str(datetime.datetime.now().day)+'/ '+str(datetime.datetime.now().month)+'/ '+str(datetime.datetime.now().year)
    if request.method=='GET':
        idPaciente = request.GET.get("pte","")
        if request.GET.get("idd","") != "":
            idDiag = request.GET.get("idd","")
        print idPaciente
        if idPaciente!="":
            Pte = Pacientes.objects.get(id=idPaciente)

    if request.method == 'POST' and request.is_ajax:
        idDiag = int(request.POST.get('IDDiag',0))

        idPaciente = request.POST.get("IDP","")
        if idPaciente!="":
            Pte = Pacientes.objects.get(id_user=idPaciente)

        text =request.POST.get("obs","")
        keys = request.POST.keys()

        doctor=Doctor.objects.get(id_user=request.user)

        dict = {'doctor':doctor.id,'paciente':idPaciente, 'text':text}
        idPresc =Preescripciones().saveWithParams(dict)

        for k in keys:
            if k != 'IDP' and k!='obs' and k!='IDDiag':
                d ={"med":k,"presc":idPresc,"indic":request.POST.get(k,"")}
                Indicaciones().saveWithParams(d)
        print idDiag
        Diagnosticos().savePrescription(idDiag=idDiag,idPresc=idPresc)
    return RenderWithUser(request=request, template="Doctor/Prescripcion.html",dict={"Fecha":fecha,"Pte":Pte,"idPrescripcion":idPresc,"idDiagnostico":idDiag}).getRendered()

@login_required
@isDoctor
def eliminarPrescripcion(request):
    print "in funcion"
    idp = request.GET.get('idp',"")
    idd = request.GET.get('idd',"")
    print idp
    print idd
    if idp != "":
        if Diagnosticos().quitPrescription(idDiag=idd,idPresc=idp):
            presc = Preescripciones.objects.get(id = idp)
            presc.delete()
            return HttpResponse("True");
    return HttpResponse("False");

@login_required
@isDoctor
def obtenerDatosPrescripcion(request):
    Doc=Doctor()
    Pte=[]
    Meds=[]
    NameM=[]
    Ind=[]
    Pres=Preescripciones()
    id_prescripcion = request.GET.get("idp","")
    if id_prescripcion != "":
        Pres = Preescripciones.objects.get(id=id_prescripcion)
        Doc = Doctor.objects.get(id=Pres.id_user.id)
        Pte = Pacientes.objects.get(id=Pres.id_paciente.id)
        Ind = Indicaciones.objects.filter(id_Presc=Pres.id)
        for i in Ind:
            m = Medicamento.objects.get(id = i.id_Medicamento.id)
            Meds.append(m)
            n = NombreM.objects.get(id = m.id_Nombre.id)
            if not NameM.__contains__(n):
                NameM.append(n)

    dict={'Doc':Doc,'Pte':Pte,'Meds':Meds,'NameM':NameM,'Ind':Ind,'Pres':Pres,'idDiagnostico':request.GET.get("idd",0)}

    return dict

@login_required
@isDoctor
def vistaPrescripcion(request):
    dict=obtenerDatosPrescripcion(request)
    return RenderWithUser(request=request, template="Doctor/vistaPrescripcion.html",dict=dict).getRendered()

@login_required
@isDoctor
def ImprimirPrescripcion(request):
    dict=obtenerDatosPrescripcion(request)
    return RenderWithUser(request=request, template="Doctor/printPrescripcion.html",dict=dict).getRendered()

@login_required
@isDoctor
def vistaDiagnostico(request):
    Doc = Doctor()
    Diag = Diagnosticos()
    Pte = Pacientes()
    isPresc = False

    id_diagnostico = request.GET.get("idd","")

    if id_diagnostico !="":
        Diag = Diagnosticos.objects.get(id = id_diagnostico)
        Doc = Doctor.objects.get(id = Diag.id_user.id)
        Pte = Pacientes.objects.get(id = Diag.id_paciente.id)

        if Diag.id_presc is not None:
            print "presc not none"
            isPresc = True

    dict={'Doc':Doc,'Pte':Pte, 'Diag':Diag,'isPresc':isPresc}
    return RenderWithUser(request=request, template="Doctor/vistaDiagnostico.html",dict=dict).getRendered()

def eliminarDiagnostico(request):
    idd = request.GET.get('idd',"")
    if idd != "":
        diag = Diagnosticos.objects.get(id=idd)
        if diag.id_presc is not None:
            idp = Preescripciones.objects.get(id=diag.id_presc.id)
            if idp != "":
                if Diagnosticos().quitPrescription(idDiag=diag.id,idPresc=idp.id):
                    idp.delete()
        diag.delete()
        return HttpResponse("True");
    return HttpResponse("False");