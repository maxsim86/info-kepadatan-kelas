# forms.py
from django import forms
from .models import ListSekolah

class InfoFilterForm(forms.Form):
    category = forms.CharField(required=False)
    
class InfoSelectForm(forms.Form):
    listsekolah = forms.ModelChoiceField(queryset=ListSekolah.objects.all(), empty_label=None)

    
class StudentColorForm(forms.Form):
    SCHOOL_CHOICES = [
        ('A', 'SMK TAMAN KLANG UTAMA'),
        ('B', 'SK TOK MUDA'),
        ('C', 'SK TELOK MENEGUN'),
        ('D', 'SK SUNGAI BINJAI')
    ]

    YEAR_CHOICES = [
        ('0', 'Pra Sekolah'),
        ('1', 'Tahun 1'),
        ('2', 'Tahun 2'),
        ('3', 'Tahun 3'),
        ('4', 'Tahun 4'),
        ('5', 'Tahun 5'),
    ]

    sekolah = forms.ChoiceField(choices=SCHOOL_CHOICES)
    tahun = forms.ChoiceField(choices=YEAR_CHOICES)
    purata = forms.IntegerField()