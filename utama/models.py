from django.db import models
from django.core.validators import RegexValidator


# Maklumat info Pelajar
class Info(models.Model):
    name = models.CharField(max_length=200, help_text="sila masukkan nama penuh seperti dalam mykid", null=True, blank=False, verbose_name='Nama')
    phone_no_regex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    no_tel = models.CharField(validators=[phone_no_regex], max_length=16, unique=True, help_text='Masukkan No Telefon', verbose_name='Nombor Telefon')
    no_ic = models.CharField(max_length=12, help_text='Nombor mykid', verbose_name='No. My Kid')
    email = models.EmailField(max_length=255)
    jum_kelas = models.IntegerField(default=0, verbose_name='jumlah kelas')
    jum_murid = models.IntegerField(default=0, verbose_name='Masukkan Jumlah Murid')
    purata = models.IntegerField(default=0)
    
    
    def __str__(self):
        return self.name
    
# Nama Sekolah dan kod sekolah.
class ListSekolah(models.Model):
    nama_sek = models.CharField(max_length=255, verbose_name='Nama Sekolah')
    kod_sekolah = models.CharField(max_length=8)

    def __str__(self):
        return self.nama_sek

# Maklumat pilihan sekolah mengikut tahun
class TahunModel(models.Model):
    YEAR_CHOICES = [
        ('Pra Sekolah', 'Pra Sekolah'),
        ('Tahun 1', 'Tahun 1'),
        ('Tahun 2', 'Tahun 2'),
        ('Tahun 3', 'Tahun 3'),
        ('Tahun 4', 'Tahun 4'),
        ('Tahun 5', 'Tahun 5'),
    ]
    tahun = models.CharField(max_length=11, default='Tahun 1', choices=YEAR_CHOICES)

    def __str__(self):
        return self.tahun