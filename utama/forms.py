# forms.py
from django import forms

class InfoFilterForm(forms.Form):
    category = forms.CharField(required=False)
    # tambahkan field lain sesuai kebutuhan
