__author__ = 'cristian'
# -*- coding: utf-8 -*-

from django.db import models as m
from django.contrib.auth.models import User

# Create your models here.
class Hospital(m.Model):
    razon = m.CharField(max_length=100)
    rfc = m.CharField(max_length=25)
    numero = m.IntegerField()
    calle = m.CharField(max_length=40)
    colonia = m.CharField(max_length=30)
    municipio = m.CharField(max_length=20)
    estado = m.CharField(max_length=20)



class GUser(m.Model):
    id_user = m.ForeignKey(User)
    name = m.CharField('Nombre', max_length=20)
    apaterno = m.CharField('Apellido Paterno', max_length=20)
    amaterno = m.CharField('Apellido Materno', max_length=20)

    class Meta:
        abstract = True
        #ordering = ['-apaterno', 'amaterno', 'name']

    def iContains(self, name):
        name = name.lower()
        tmpName = self.name + self.apaterno + self.amaterno
        tmpName = tmpName.lower()
        return tmpName.__contains__(name)

class HUser(GUser):
    fech_naci = m.DateField('F. Nacimiento')
    calle = m.CharField('Calle', max_length=40)
    numero = m.IntegerField('Número')
    colonia = m.CharField(max_length=40)
    cod_post = m.IntegerField('C. P.')
    municipio = m.CharField(max_length=20)
    estado = m.CharField(max_length=20)
    pais = m.CharField('País', max_length=20)
    tel = m.CharField('Teléfono', max_length=15)
    cel = m.CharField('Celular', max_length=15)

    class Meta:
        abstract = True

class TipoUsuario(m.Model):
    id_user = m.ForeignKey(User)
    tipo = m.SmallIntegerField()

    def saveWithParams(self, dict = None):
        if dict is None:
            raise Exception('Necesita pasar un diccionario para la creacion del tipo')
        try:
            self.id_user = dict['user']
            self.tipo = dict['tipo']
            self.save()
        except KeyError:
            raise Exception('Imposible crear el tipo, faltan parametros')