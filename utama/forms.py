# forms.py
from django import forms
from .models import ListSekolah
from .models import Info
from django.contrib import admin

class InfoFilterForm(forms.Form):
    category = forms.CharField(required=False)
    
class InfoSelectForm(forms.Form):
    listsekolah = forms.ModelChoiceField(queryset=ListSekolah.objects.all(), empty_label=None)

class AdminStudentColorForm(forms.ModelForm):
    class Meta:
        model = Info
        fields = '__all__'
    
class StudentColorForm(forms.ModelForm):
    class Meta:
        model = Info
        fields = '__all__'
        widgets = {
            'purata': forms.HiddenInput(),
            'jum_kelas':forms.HiddenInput(),
            'jum_murid':forms.HiddenInput(),
        }
        

    YEAR_CHOICES = [
        ('0', 'Pra Sekolah'),
        ('1', 'Tahun 1'),
        ('2', 'Tahun 2'),
        ('3', 'Tahun 3'),
        ('4', 'Tahun 4'),
        ('5', 'Tahun 5'),
    ]

    sekolah = forms.ModelChoiceField(queryset=ListSekolah.objects.all())
    tahun = forms.ChoiceField(choices=YEAR_CHOICES)
    jum_kelas = forms.TypedChoiceField(coerce=int, choices=[(i, i) for i in range(1, 15)])
    jum_murid = forms.IntegerField()
    purata = forms.FloatField(widget=forms.HiddenInput(), required=False)
    catatan = forms.CharField(widget=forms.TextInput())

    def clean(self):
        cleaned_data = super().clean()
        jum_kelas = cleaned_data.get('jum_kelas')
        jum_murid = cleaned_data.get('jum_murid')
        
        # Lakukan calculator
        if jum_murid > 0:
            purata = jum_murid / jum_kelas
            cleaned_data['purata'] = purata
        else:
            # Set purata kepada 0 if jum_murid adalah 0
            cleaned_data['purata'] = 0
        return cleaned_data

# Register the new form for the admin
class InfoAdmin(admin.ModelAdmin):
    form = AdminStudentColorForm

admin.site.register(Info, InfoAdmin)
#admin.site.register(ListSekolah)

