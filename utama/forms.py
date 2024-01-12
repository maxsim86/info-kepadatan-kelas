# forms.py
from django import forms
from .models import ListSekolah, TahunModel
from .models import Info
from django.contrib import admin


class InfoSelectForm(forms.Form):
    listsekolah = forms.ModelChoiceField(
        queryset=ListSekolah.objects.all(), empty_label=None
    )


class AdminStudentColorForm(forms.ModelForm):
    class Meta:
        model = Info
        fields = "__all__"


class StudentColorForm(forms.ModelForm):
    class Meta:
        model = Info
        fields = [
            "name",
            "no_tel",
            "no_ic",
            "email",
            "jum_kelas",
            "jum_murid",
            "purata",
            "tahun",
            "list_sek",
        ]

        widgets = {
            #"jum_kelas": forms.HiddenInput(),
            #"jum_murid": forms.HiddenInput(),
            "purata": forms.HiddenInput(),
            "name": forms.TextInput(attrs={'placeholder':'Nama Penuh', 'size':35, 'title':'Masukkan Nama Penuh Anda!'}),
            "no_tel": forms.TextInput(attrs={'placeholder': 'Nomber Telefon', 'size': 35}),
            "email": forms.EmailInput(attrs={'placeholder':'E-mail','size':35, 'title': 'Masukkan Email cth : simbad@gmail.com'}),
            "no_ic": forms.NumberInput(attrs={'placeholder':'Nombor MYKID', 'size':35}),

        }

        # overrite init , call super ini

    tahun = forms.ModelChoiceField(
        queryset=TahunModel.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    
    jum_kelas = forms.IntegerField(label='jumlah kelas',required=False)
    
    jum_murid = forms.IntegerField(label='jumlah murid', required=False )
    
    purata = forms.FloatField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["jum_kelas"]

    def clean(self):
        cleaned_data = super().clean()
        jum_kelas = cleaned_data.get("jum_kelas", 0)
        jum_murid = cleaned_data.get("jum_murid", 0)
        # Convert to jum_kelas to integer
        jum_kelas = int(jum_kelas) if jum_kelas else 0
        # Convert to jum_murid to integer
        jum_murid = int(jum_murid) if jum_murid else 0

        # Lakukan calculator
        if jum_murid > 0:
            purata = jum_murid / jum_kelas
            cleaned_data["purata"] = purata
        else:
            # Set purata kepada 0 if jum_murid adalah 0
            cleaned_data["purata"] = 0
        return cleaned_data


# Register the new form for the admin
class InfoAdmin(admin.ModelAdmin):
    form = AdminStudentColorForm
    list_display = ("tahun", "jum_kelas", "jum_murid", "purata")


admin.site.register(Info, InfoAdmin)


# admin.site.register(ListSekolah)
class SCVUploadForm(forms.Form):
    csv_file = forms.FileField()
