from django.forms import ModelForm
from HPatients.models import Diagnosticos, Preescripciones, Indicaciones

class DiagnosisForm(ModelForm):
    class Meta:
        model = Diagnosticos
        exclude = ['id_user', 'id_paciente','id_presc','fech','hora']

    def __init__(self, *args, **kwargs):
        super(DiagnosisForm, self).__init__(*args, **kwargs)

class PrescForm(ModelForm):
    class Meta:
        model = Preescripciones
        exclude = ['id_user', 'id_paciente']

    def __init__(self, *args, **kwargs):
        super(PrescForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class' : 'indicacion'})

class IndiForm(ModelForm):
    class Meta:
        model = Indicaciones
        exclude = ['id_Medicamento', 'id_Presc']

    def __init__(self,num, *args, **kwargs):
        super(IndiForm, self).__init__(*args, **kwargs)
        self.fields['indicacion'].widget.attrs.update({'class' : 'indicacion','id':'indicacion'+num})