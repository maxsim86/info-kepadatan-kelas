from django import forms
from .models import Classroom

class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['school']
        
class ContactForm(forms.Form):
    name = forms.CharField(label='Nama', max_length=200, required=False)
    email = forms.EmailField(label='Email', required=False)
    message = forms.CharField(label='Mesej Anda', max_length=300, widget=forms.Textarea)