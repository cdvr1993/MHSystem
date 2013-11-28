# -*- coding: utf-8 -*-
__author__ = 'esteban'

from django.forms import ModelForm
from models import Administrador
from django.contrib.auth.models import User

class PermissionForm(ModelForm):
    class Meta:
        from HDoctors.models import Permisos
        model = Permisos
        exclude = ['id_user']

    def __init__(self, *args, **kwargs):
        super(PermissionForm, self).__init__(*args, **kwargs)

class AdministradorForm(ModelForm):
    class Meta:
        model = Administrador
        exclude = ['id_user']

    def __init__(self, *args, **kwargs):
        super(AdministradorForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class' : 'myfieldclass'})

class Doctorform(AdministradorForm):
    class Meta:
        from HDoctors.models import Doctor
        model = Doctor
        exclude = ['id_user']

    def __init__(self, *args, **kwargs):
        super(Doctorform, self).__init__(*args, **kwargs)
        self.fields['fech_naci'].widget.input_type = 'date'

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = 'E-mail'
        self.fields['password'].widget.input_type = 'password'

class EmailForm(ModelForm):
    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = 'E-mail'
        self.fields['email'].required = True