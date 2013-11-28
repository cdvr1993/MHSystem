# -*- coding: utf-8 -*-

from django.db import models as m
from DDS.models import HUser

class Doctor(HUser):
    matricula = m.CharField('Matrícula', max_length=20)
    especialidad = m.CharField(max_length=30)
    area = m.CharField('Área', max_length=30)

    class Meta:
        ordering = ['apaterno', 'amaterno', 'name']

    def saveWithParams(self, dict = None):
        if dict is None:
            raise Exception('Hace falta el diccionaario con los parametros')
        self.id_user = dict['user']
        self.insertDict(dict)
        dict.update({'tipo' : 2})
        from DDS.models import TipoUsuario as Type
        Type().saveWithParams(dict)
        Permisos().saveWithParams({'id_user' : self, 'acceso' : dict['acceso'], 'full_view' : dict['full_view']})

    def Update(self, id = -1, dict = None):
        if id == -1:
            raise Exception('Falta el id para actualizar')
        self = Doctor.objects.get(id_user=id)
        self.insertDict(dict)

    def insertDict(self, dict = None):
        if dict is None:
            raise Exception('Falta diccionario de actualizacion')
        from DDS.utils import CapitalizeDict
        CapitalizeDict(dict)
        self.name = dict.get('name', self.name)
        self.apaterno = dict.get('apaterno', self.apaterno)
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
        self.especialidad = dict.get('especialidad', self.especialidad)
        self.matricula = dict.get('matricula', self.matricula)
        self.area = dict.get('area', self.area)
        self.cod_post = dict.get('cod_post', self.cod_post)
        self.save()

class Permisos(m.Model):
    id_user = m.ForeignKey(Doctor)
    acceso = m.BooleanField('Acceso al sistema')
    full_view = m.BooleanField('Ver todos los pacientes')

    def saveWithParams(self, dict = None):
        self.id_user = dict['id_user']
        self.insertDict(dict)

    def Update(self, id = - 1, dict = None):
        if id == -1:
            raise Exception('No se ha asignado un ID para actualizar')
        self = Permisos.objects.get(id_user=Doctor.objects.get(id_user=id))
        self.insertDict(dict)

    def insertDict(self, dict = None):
        if dict is None:
            raise Exception('El diccionario de permisos no contiene parametros')
        self.acceso = dict['acceso']
        self.full_view = dict['full_view']
        self.save()

class TipoAnalisis(m.Model):
    pass

def getCount():
    return Doctor.objects.filter(id_user__is_active=True).count()