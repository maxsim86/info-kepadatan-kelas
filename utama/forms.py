# forms.py
from django import forms
from .models import ListSekolah

class InfoFilterForm(forms.Form):
    category = forms.CharField(required=False)
    
class InfoSelectForm(forms.Form):
    listsekolah = forms.ModelChoiceField(queryset=ListSekolah.objects.all(), empty_label=None)



    
class StudentColorForm(forms.Form):
    SCHOOL_CHOICES = [
        ('A', 'School A'),
        ('B', 'School B'),
    ]

    YEAR_CHOICES = [
        ('1', 'Year 1'),
        ('2', 'Year 2'),
        ('3', 'Year 3'),
        ('4', 'Year 4'),
        ('5', 'Year 5'),
    ]

    school = forms.ChoiceField(choices=SCHOOL_CHOICES)
    year = forms.ChoiceField(choices=YEAR_CHOICES)
    score = forms.IntegerField()