# -*- coding: utf-8 -*-

from django import forms as f
from django.forms import ModelForm
from HAdmin.forms import Doctorform
from HPatients.models import Pacientes

class PatientForm(Doctorform):
    class Meta:
        model = Pacientes
        exclude = ['id_user', 'id_doctor']

    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        self.fields['enfermedades'].required = False
        self.fields['alergias'].required = False
        self.fields['discapacidad'].required = False
        self.fields['antecedentes'].required = False

from django.core.exceptions import ValidationError

def maxSize(file):
    from DDS.settings import FILE_UPLOAD_MAX_MEMORY_SIZE
    if file.size > FILE_UPLOAD_MAX_MEMORY_SIZE:
        raise ValidationError(u"Excede el tamaño máximo")

def extension(file):
    no = file.name
    if no[-4 : ] != '.pdf':
        raise ValidationError(u'Solo se aceptan archivos pdf')

class UploadForm(f.Form):
    name = f.CharField(max_length=60)
    file = f.FileField(validators=[maxSize, extension])
    fech = f.DateField()

    def __init__(self, *args, **kwargs):
        super(UploadForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Nombre'
        self.fields['file'].label = 'Archivo'
        self.fields['fech'].label = 'Fecha del Análisis'
        self.fields['fech'].widget.input_type = 'date'

from DDS.forms import SearchByDate
class HistorialSearch(SearchByDate):
    name = f.CharField(max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        super(HistorialSearch, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Nombre'