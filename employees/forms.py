from django.forms import ModelForm
from employees.models import fPonto, dColaboradores
from django.utils import timezone
from django import forms


class fPontoForm(ModelForm):
    class Meta:
        model = fPonto
        fields = ['idColaborador', 
                  'data',
                ]
        labels = {
            'idColaborador': 'Colaborador',
            'data': 'Data',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['idColaborador'].queryset = dColaboradores.objects.all()

        self.fields['data'].widget = forms.DateTimeInput(attrs={'name' : 'idColaborador'})
        self.fields['data'].initial = timezone.now()
        self.fields['data'].widget = forms.DateTimeInput(attrs={'type' : 'datetime', 'readonly': True, 'name' : 'data', 'id': 'labelForm'})

