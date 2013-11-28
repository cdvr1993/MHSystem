# -*- coding: utf-8 -*-

#   Django
from django.conf import settings
from django.conf.urls import patterns #, include, url
# Archivos estáticos
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DDS.views.home', name='home'),
    # url(r'^DDS/', include('DDS.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    #   Generales
    (r'^$', 'DDS.main.actionLogin'),
    (r'^logout/$', 'DDS.main.actionLogout'),
    (r'^saveKey/$', 'DDS.main.SaveKey'),
    (r'^decodeData/$', 'DDS.main.DecodeData'),
    (r'^login/$', 'DDS.main.actionIndex'),
    #   Administrador
    (r'^administrator/$', 'HAdmin.Administrador.HomeAdministrador'),
    (r'^administrator/ListaDeUsuarios', 'HAdmin.Administrador.ListaDeUsuarios'),
    (r'^administrator/adminPaginator', 'HAdmin.Administrador.AdminPaginador'),
    (r'^administrator/doctorPaginator', 'HAdmin.Administrador.DoctorPaginador'),
    (r'^administrator/ListaDeAdmins/$', 'HAdmin.Administrador.ListadoDeAdministradores'),
    (r'^administrator/ListaDeDoctores/$', 'HAdmin.Administrador.ListadoDeDoctores'),
    (r'^administrator/EditUser/$', 'HAdmin.Administrador.EditUser'),
    (r'^administrator/DeleteUser/$', 'HAdmin.Administrador.DeleteUser'),
    (r'^administrator/RegisterAdmin', 'HAdmin.Administrador.RegisterAdmin'),
    (r'^administrator/RegisterDoctor/$', 'HAdmin.Administrador.RegistrarDoctor'),
    #   Doctores
    (r'^doctor/$', 'HDoctors.Doctores.HomeDoctor'),
    (r'^doctor/Upload/$', 'HDoctors.Doctores.UploadRequest'),
    (r'^doctor/Historial/$', 'HDoctors.Doctores.Historial'),
    (r'^doctor/Historial/Filter/$', 'HDoctors.Doctores.getHistorialFilter'),
    (r'^doctor/RegistrarPaciente/$', 'HDoctors.Doctores.RegisterPatient'),
    (r'^doctor/ListaDePacientes/$', 'HDoctors.Doctores.ListadoDePacientes'),
    (r'^doctor/ListaGralPacientes/$', 'HDoctors.Doctores.ListadoGralPacientes'),
    (r'^doctor/EditUser/$', 'HDoctors.Doctores.EditUser'),
    (r'^doctor/DeleteUser/$', 'HDoctors.Doctores.DeleteUser'),
    (r'^doctor/myPatientPaginator/$', 'HDoctors.Doctores.MyPatientPaginador'),
    (r'^doctor/patientPaginator/$', 'HDoctors.Doctores.PatientPaginator'),
    (r'^doctor/searchPatient/$', 'HDoctors.Doctores.selectionB'),
    (r'^doctor/diagnostico/$', 'HDoctors.Doctores.Diagnostico'),
    (r'^doctor/prescripcion/$', 'HDoctors.Doctores.Prescripciones'),
    (r'^doctor/medicamentos/$', 'HDoctors.Doctores.searchMeds'),
    (r'^doctor/vistaPrescripcion/$', 'HDoctors.Doctores.vistaPrescripcion'),
    (r'^doctor/vistaDiagnostico/$', 'HDoctors.Doctores.vistaDiagnostico'),
    (r'^doctor/deletePrescripcion/$', 'HDoctors.Doctores.eliminarPrescripcion'),
    (r'^doctor/printPrescripcion/$', 'HDoctors.Doctores.ImprimirPrescripcion'),
    (r'^doctor/deleteDiagnostico/$', 'HDoctors.Doctores.eliminarDiagnostico'),
    #   Pacientes
    (r'^patient/$', 'HPatients.Pacientes.HomePaciente'),
    (r'^patient/Historial/$', 'HPatients.Pacientes.Historial'),
    (r'^patient/Historial/Filter/$', 'HPatients.Pacientes.HistorialFilter'),
    (r'^patient/MisAnalisis/$', 'HPatients.Pacientes.MisAnalisis'),
    (r'^patient/MisAnalisis/getFile/$', 'HPatients.Pacientes.getFile'),
    (r'^patient/MisAnalisis/search/$', 'HPatients.Pacientes.searchAnalisis'),
    (r'^patient/vistaDiagnostico/$', 'HPatients.Pacientes.vistaDiagnostico'),
    (r'^patient/vistaPrescripcion/$', 'HPatients.Pacientes.vistaPrescripcion'),
    # Solo para pruebas
    (r'^Error/$', 'DDS.test.NotAuthorized'),
    (r'^DelUser/$', 'DDS.test.DelUser'),
    (r'^Test/Activate/$', 'DDS.test.activateUser'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) #\
              #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
