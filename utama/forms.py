from django import forms
from .models import Classroom
from django.forms import ModelForm

class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['school']
        widgets = {
            'school':forms.Select(attrs={'class':'form-select', 'style':'max-width:300px'}),
        }
        

class ImportForm(forms.Form):
    file = forms.FileField()
    