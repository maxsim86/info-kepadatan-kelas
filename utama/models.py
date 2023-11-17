from django.db import models
from django.core.validators import RegexValidator

# Create your models here.



class Info(models.Model):
    name = models.CharField(max_length=200)
    phone_no_regex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    no_tel = models.CharField(validators=[phone_no_regex], max_length=16, unique=True)
    no_ic = models.CharField(max_length=12)
    email = models.EmailField(max_length=50)
    category = models.CharField(max_length=100)
    
    # Level tingkatan peringkat sekolah !
    TINGKATAN_1 = "TINGKATAN 1"
    TINGKTAN_2 = "TINGKATAN 2"
    TINGKATAN_3 = "TINGKATAN 3" 
    TINGKATAN_4 = "TINGKATAN 4"
    TINGKATAN_5 = "TINGKATAN 5"

    PILIHAN_LEVEL_SEKOLAH =[
        (TINGKATAN_1, "Tingkatan 1"),
        (TINGKTAN_2, "Tingkatan 2"),
        (TINGKATAN_3, "Tingkatan 3"),
        (TINGKATAN_4, "Tingkatan 4"),
        (TINGKATAN_5, "Tingkatan 5"),
    ]
    level_tingkatan = models.CharField(max_length=12, choices=PILIHAN_LEVEL_SEKOLAH,default=TINGKATAN_1)

    
    def __str__(self):
        return self.name