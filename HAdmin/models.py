from django.db import models as m
from DDS.models import GUser, TipoUsuario as Type

class Administrador(GUser):
    puesto = m.CharField(max_length=30)

    class Meta:
        ordering = ['apaterno', 'amaterno', 'name']

    def strName(self):
        return self.name + ' ' + self.apaterno

    def saveWithParams(self, dict = None):
        self.id_user=dict['user']
        self.inserDict(dict)
        dict.update({'tipo' : 1})
        Type().saveWithParams(dict)

    def Update(self, id = -1, dict = None):
        if id == -1:
            raise Exception('Falta el id para actualizar')
        self = Administrador.objects.get(id_user=id)
        self.inserDict(dict)

    def inserDict(self, dict = None):
        if dict is None:
            raise Exception('Falta diccionario para guardar atributos')
        from DDS.utils import CapitalizeDict
        CapitalizeDict(dict)
        self.name = dict.get('name', self.name)
        self.apaterno = dict.get('apaterno', self.name)
        self.amaterno = dict.get('amaterno', self.amaterno)
        self.puesto = dict.get('puesto', self.puesto)
        self.save()

def getCount():
    return Administrador.objects.filter(id_user__is_active=True).count()