from django import forms
from .models import Classroom, Contact_us
from django.forms import ModelForm

class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['school']
        

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact_us
        fields = '__all__'
        widgets = {'message': forms.Textarea(attrs={"cols": 80, "row": 20})}
        labels = {
            'name':'Nama',
            'email':'E-mail',
            'message':'Mesej'
        }

class ImportForm(forms.Form):
    file = forms.FileField()
    