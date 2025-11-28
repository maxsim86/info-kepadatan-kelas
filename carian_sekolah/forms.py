from django import forms
from .models import SchoolImageSubmission


class ImageSubmissionForm(forms.ModelForm):
    class Meta:
        model = SchoolImageSubmission
        # Kita hanya mahu pengguna memuat naik gambar.
        # Medan 'school' dan 'status' akan diuruskan secara automatik.
        fields = ["image"]
        labels = {"image": "Pilih fail gambar sekolah"}
