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
        fields = ['name', 'email', 'message']
        widgets = {'message': forms.Textarea(attrs={"cols": 80, "row": 20})}
