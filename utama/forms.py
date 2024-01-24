from django import forms
from .models import Classroom

class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['school']
        
        
class ContactForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100)
    email = forms.EmailField(label='Your Email')
    message = forms.CharField(label='Your Message', widget=forms.Textarea)