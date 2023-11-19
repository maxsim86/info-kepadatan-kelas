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
    
    # Level tingkatan peringkat sekolah !
    PPKI = "PPKI"
    TAHUN_1 = "TAHUN 1"
    TAHUN_2 = "TAHUN 2" 
    TAHUN_3 = "TAHUN 3"
    TAHUN_4 = "TAHUN 4"
    TAHUN_5 = "TAHUN 5"

    PILIHAN_LEVEL_SEKOLAH =[
        (PPKI, "PPKI"),
        (TAHUN_1, "Tahun 1"),
        (TAHUN_2, "Tahun 2"),
        (TAHUN_3, "Tahun 3"),
        (TAHUN_4, "Tahun 4"),
        (TAHUN_5, "Tahun 5"),
    ]
    level_tingkatan = models.CharField(max_length=12, choices=PILIHAN_LEVEL_SEKOLAH,default=TAHUN_1)
    
    def __str__(self):
        return f"{self.get_level_tingkatan_display()}"
    
class ListSekolah(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name