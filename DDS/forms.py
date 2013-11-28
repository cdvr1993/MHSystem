# -*- coding: utf-8 -*-
__author__ = 'cristian'

from django import forms as f

class SearchByDate(f.Form):
    init = f.DateField()
    final = f.DateField()

    def __init__(self, *args, **kwargs):
        super(SearchByDate, self).__init__(*args, **kwargs)
        self.fields['init'].widget.input_type = 'date'
        self.fields['init'].label = 'Fecha inicial'
        self.fields['init'].widget.attrs.update({'onchange' : 'validateDate(this)'})
        self.fields['final'].widget.input_type = 'date'
        self.fields['final'].label = 'Fecha final'
        self.fields['final'].widget.attrs.update({'onchange' : 'validateDate(this)'})

