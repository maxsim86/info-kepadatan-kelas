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
    

    
class ListSekolah(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name