# -*- coding: utf-8 -*-
__author__ = 'cristian'
from django.http import HttpResponse
from DDS.utils import RenderWithUser
from django.contrib.auth.decorators import login_required
from models import Pacientes, Analisis, Preescripciones, Indicaciones, Medicamento, Diagnosticos, NombreM
from HDoctors.models import Doctor
from django.http import Http404
from DDS.utils import isPatient

@login_required
@isPatient
def HomePaciente(request):
    # Regresa la página de inicio del Paciente
    patient = Pacientes.objects.get(id_user=request.user)
    return RenderWithUser(request=request, template="Paciente/index.html", dict={'Patient' : patient }).getRendered()

@login_required
@isPatient
def MisAnalisis(request):
    # Página que muestra el form de búsqueda de Analisis y también muestra los resultados
    anl = Analisis.objects.filter(id_paciente=Pacientes.objects.get(id_user=request.user)).order_by('fech', 'path')
    from DDS.forms import SearchByDate
    anreq = AnalisisRequest().appendFilter(anl)
    return  RenderWithUser(request=request, template="Paciente/MisAnalisis.html", dict={ 'Files' : anreq, 'sForm' : SearchByDate }).getRendered()

@login_required
@isPatient
def getFile(request):
    # Función que a partir de un id regresa un PDF con apoyo de openPDF
    id = request.GET.get('file', None)
    if id is None:
        raise Http404
    return openPDF(Analisis.objects.get(pk=id).path)

def openPDF(path):
    # Función que maneja el poder abrir pdfs y regresarlos en un objeto response
    f = open(path)
    response = HttpResponse(f, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="somefilename.pdf"'
    return response

@login_required
@isPatient
def searchAnalisis(request):
    # Función que maneja la búsqueda de Análisis en base a las fechas
    from DDS.forms import SearchByDate
    if request.method == 'POST':
        init = request.POST['init']
        final = request.POST['final']
        from DDS.utils import GetDateRange
        range = [init, final]
        GetDateRange(Analisis, range)
        sForm = SearchByDate({ 'init' : range[0] , 'final' : range[1] })
        if sForm.is_valid():
            d = sForm.cleaned_data
            anl = Analisis.objects.filter(id_paciente=Pacientes.objects.get(id_user=request.user)).filter(fech__range=(d['init'], d['final'])).order_by('fech', 'path')
            anreq = AnalisisRequest().appendFilter(anl)
            return RenderWithUser(request=request, template="Paciente/ListaDeAnalisis.html", dict={ 'Files' : anreq }).getRendered()
    raise Http404

@login_required
@isPatient
def vistaDiagnostico(request):
    isPresc = False
    id_diagnostico = request.GET.get("idd","")
    if id_diagnostico != "":
        Diag = Diagnosticos.objects.get(id = id_diagnostico)
        Doc = Doctor.objects.get(id = Diag.id_user.id)
        Pte = Pacientes.objects.get(id = Diag.id_paciente.id)
        if Diag.id_presc is not None:
            isPresc = True
        dict={'Doc':Doc,'Pte':Pte, 'Diag':Diag,'isPresc':isPresc}
        return RenderWithUser(request=request, template="Paciente/vistaDiagnostico.html",dict=dict).getRendered()
    raise Http404

@login_required
@isPatient
def vistaPrescripcion(request):
    dict=obtenerDatosPrescripcion(request)
    return RenderWithUser(request=request, template="Paciente/vistaPrescripcion.html",dict=dict).getRendered()

@login_required
@isPatient
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
            NameM.append(n)

    dict={'Doc':Doc,'Pte':Pte,'Meds':Meds,'NameM':NameM,'Ind':Ind,'Pres':Pres,'idDiagnostico':request.GET.get("idd",0)}

    return dict

@login_required
@isPatient
def Historial(request):
    # Mostrará el formulario de búsqueda donde posteriormente se agregarán los resultados de la búsqueda
    from DDS.forms import SearchByDate
    if request.method == 'GET':
        return RenderWithUser(request=request, template="Paciente/Historial.html", dict={ 'sForm' : SearchByDate }).getRendered()
    raise Http404

@login_required
@isPatient
def HistorialFilter(request):
    # Obtendrá los resultados conforme a los parámetros envíados mediante javascript
    d = request.GET
    try:
        rango = [d['init'], d['final']]
    except Exception:
        return HttpResponse('')
    from DDS.utils import GetDateRange
    from models import Diagnosticos
    from DDS.forms import SearchByDate
    from django.shortcuts import render_to_response
    GetDateRange(Diagnosticos, rango)
    sD = SearchByDate({ 'init' : rango[0], 'final' : rango[1]})
    if sD.is_valid():
        d = sD.cleaned_data
        diag = Diagnosticos.objects.filter(id_paciente=Pacientes.objects.get(id_user=request.user)).filter(fech__range=(rango[0], rango[1]))
        return render_to_response("Paciente/TableDiagnosticos.html", {'diagnosticos' : diag})

class AnalisisRequest:
    # Clase que manejará el objeto de Analisis y el nombre que se obtiene manualmente
    class AnalisisTmp:
        def __init__(self, analisis, name):
            self.analisis = analisis
            self.name = name

    def __init__(self):
        self.files = []

    def appendFilter(self, filter):
        for entry in filter:
            self.files.append(AnalisisRequest.AnalisisTmp(entry, entry.path[entry.path.rfind("/") + 1:]))
        return self.files