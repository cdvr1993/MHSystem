# -*- coding: utf-8 -*-
from django.db import models as m
from DDS.models import HUser
from HDoctors.models import Doctor

# Create your models here.
class Pacientes(HUser):
    SANGRE_CHOICES = (('A+','A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-'))
    id_doctor = m.ForeignKey(Doctor)
    enfermedades = m.TextField(blank=True)
    alergias = m.TextField('Alergías', blank=True)
    discapacidad = m.TextField('Discapacidades', blank=True)
    antecedentes = m.TextField(blank=True)
    curp = m.CharField('CURP', max_length=20)
    sangre = m.CharField('Tipo de Sangre', max_length=5, choices=SANGRE_CHOICES)
    grupo = m.CharField('Grupo étnico', max_length=20)
    religion = m.CharField('Religión', max_length=30)

    class Meta:
        ordering = ['apaterno', 'amaterno', 'name']

    def saveWithParams(self, dict = None):
        if dict is None:
             raise Exception('Hace falta el diccionaario con los parametros')
        self.id_doctor=dict['doctor']
        self.id_user = dict['user']
        self.insertDict(dict)
        dict.update({'tipo':3})
        from DDS.models import TipoUsuario as Type
        Type().saveWithParams(dict)

    def Update(self, id = -1, dict = None):
        if id == -1:
            raise Exception('Falta el id para actualizar')
        self = Pacientes.objects.get(id_user=id)
        self.insertDict(dict)

    def insertDict(self, dict = None):
        if dict is None:
            raise Exception('Falta diccionario de actualizacion')
        from DDS.utils import CapitalizeDict
        CapitalizeDict(dict)
        self.name = dict.get('name', self.name)
        self.apaterno = dict.get('apaterno', self.name)
        self.amaterno = dict.get('amaterno', self.amaterno)
        self.calle = dict.get('calle', self.calle)
        self.numero = dict.get('numero', self.numero)
        self.colonia = dict.get('colonia', self.colonia)
        self.municipio = dict.get('municipio', self.municipio)
        self.estado = dict.get('estado', self.estado)
        self.pais = dict.get('pais', self.pais)
        self.fech_naci = dict.get('fech_naci', self.fech_naci)
        self.tel = dict.get('tel', self.tel)
        self.cel = dict.get('cel', self.cel)
        self.cod_post = dict.get('cod_post', self.cod_post)
        self.enfermedades = dict.get('enfermedades', self.enfermedades)
        self.alergias = dict.get('alergias', self.alergias)
        self.antecedentes = dict.get('antecedentes', self.antecedentes)
        self.discapacidad = dict.get('discapacidad', self.discapacidad)
        self.curp = dict.get('curp', self.curp)
        self.sangre = dict.get('sangre', self.sangre)
        self.grupo = dict.get('grupo', self.grupo)
        self.religion = dict.get('religion', self.religion)
        self.save()

class Preescripciones(m.Model):

    id_user = m.ForeignKey(Doctor)
    id_paciente = m.ForeignKey(Pacientes)
    fecha = m.DateField('Fecha',auto_now=True)
    text = m.TextField('Observaciones',null=True, blank=True)

    def saveWithParams(self, dict = None):
        if dict is None:
             raise Exception('Hace falta el diccionaario con los parametros')
        self.id_user = Doctor.objects.get(id=dict['doctor'])
        self.id_paciente = Pacientes.objects.get(id_user=dict['paciente'])
        self.insertDict(dict)
        return self.id


    def insertDict(self,dict=None):
        if dict is None:
             raise Exception('Hace falta el diccionaario con los parametros')
        self.text = dict.get('text',self.text)
        self.save()

class Analisis(m.Model):
    id_user = m.ForeignKey(Doctor)
    id_paciente = m.ForeignKey(Pacientes)
    fech = m.DateField()
    fech_up = m.DateField()
    tipo = m.CharField(max_length=50)
    path = m.CharField(max_length=100)

    def saveWithParams(self, dict = None):
        if dict is None:
            raise Exception('Debe especificar un diccionario para guardar el Análisis')
        self.id_user = dict['id_user']
        self.id_paciente = dict['id_paciente']
        self.fech = dict['fech']
        self.fech_up = dict['fech_up']
        self.tipo = dict['tipo']
        self.path = dict['path']
        self.save()

class Diagnosticos(m.Model):
    id_user = m.ForeignKey(Doctor)
    id_paciente = m.ForeignKey(Pacientes)
    id_presc = m.ForeignKey(Preescripciones, null=True, blank=True)
    fech = m.DateField('Fecha',auto_now=True)
    hora = m.TimeField('Hora',auto_now=True)
    text = m.TextField('Diagnóstico')

    def saveWithParams(self, dict = None):
        if dict is None:
             raise Exception('Hace falta el diccionario con los parametros para el diagnóstico')
        self.id_user = Doctor.objects.get(id=dict['doctor'])
        self.id_paciente = Pacientes.objects.get(id_user=dict['paciente'])
        self.id_presc = dict.get('presc',None)
        self.insertDict(dict)
        return self.id

    def insertDict(self,dict=None):
        if dict is None:
             raise Exception('Hace falta el diccionaario con los parametros')
        self.fech = dict.get('fech',self.fech)
        self.hora = dict.get('hora',self.hora)
        self.text = dict.get('text',self.text)
        self.save()

    def savePrescription(self, idDiag, idPresc):
        self=Diagnosticos.objects.get(pk=idDiag)
        self.id_presc = Preescripciones.objects.get(id=idPresc)
        self.save()

    def quitPrescription(self, idDiag, idPresc):
        print "in quit"
        self=Diagnosticos.objects.get(pk=idDiag)
        print self.id_presc.id
        if int(idPresc) == int(self.id_presc.id):
            print "equal"
            self.id_presc = None
            self.save()
            return True
        return False

class Grupo(m.Model):
    grupo = m.TextField()

class NombreM(m.Model):
    medicamento = m.TextField()
    id_Grupo = m.ForeignKey(Grupo, related_name="grupo_medicamento")

class Medicamento(m.Model):
    id_Nombre = m.ForeignKey(NombreM, related_name="medicamento_nombre")
    descripcion = m.TextField()
    cantidad = m.DecimalField(max_digits=7,decimal_places=3)
    unidad = m.CharField(max_length=6)
    presentacion = m.TextField()
    unidad_pres = m.CharField(max_length=50)

class Indicaciones(m.Model):
    id_Medicamento = m.ForeignKey(Medicamento,related_name="Indicaciones_medicamento")
    id_Presc = m.ForeignKey(Preescripciones, related_name="Indicaciones_presc")
    indicacion = m.TextField("Indicación")

    def saveWithParams(self, dict = None):
        if dict is None:
             raise Exception('Hace falta el diccionaario con los parametros')
        self.id_Medicamento= Medicamento.objects.get(id=dict['med'])
        self.id_Presc = Preescripciones.objects.get(id=dict['presc'])
        self.indicacion = dict.get('indic',"")
        self.save()

def getCount(filtrado = None):
    if filtrado is None:
        return Pacientes.objects.filter(id_user__is_active=True).count()
    else:
        return Pacientes.objects.filter(id_user__is_active=True).filter(id_doctor=filtrado).count()