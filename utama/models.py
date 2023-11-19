from django.db import models
from django.core.validators import RegexValidator

# Create your models here.


class Info(models.Model):
    name = models.CharField(max_length=200)
    phone_no_regex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    no_tel = models.CharField(validators=[phone_no_regex], max_length=16, unique=True)
    no_ic = models.CharField(max_length=12)
    email = models.EmailField(max_length=255)
    category = models.CharField(max_length=100)
    jum_kelas = models.IntegerField(default=0)
    jum_murid = models.IntegerField(default=0)
    purata = models.IntegerField(default=0)
    catatan = models.TextField(max_length=255)
    
    def __str__(self):
        return self.name
    
# Nama Sekolah dan kod sekolah.
class ListSekolah(models.Model):
    name = models.CharField(max_length=255)
    kod_sekolah = models.CharField(max_length=8)

    def __str__(self):
        return self.name

    
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