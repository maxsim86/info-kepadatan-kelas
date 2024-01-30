from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 

class Classroom(models.Model):
    SCHOOL_CHOICES = [
        ('SK KLANG', 'SK KLANG'),
        ('SK TELOK GADONG', 'SK TELOK GADONG'),
        ('SK PELABUHAN KLANG', 'SK PELABUHAN KLANG'),

    ]
    YEAR_CHOICES = [
            ('PPKI', 'PPKI'),
            ('TAHUN1', 'TAHUN1'),
            ('TAHUN2', 'TAHUN2'),
            ('TAHUN3', 'TAHUN3'),
            ('TAHUN4', 'TAHUN4'),
            ('TAHUN5', 'TAHUN5'),
            ('TAHUN6', 'TAHUN6'),
    ]

    school = models.CharField(max_length=50, choices=SCHOOL_CHOICES, verbose_name='Pilihan Sekolah')
    year = models.CharField(max_length=10, choices= YEAR_CHOICES, verbose_name='tahun kelas')
    average = models.IntegerField(verbose_name='purata')
    last_update = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Enrolmen Sekolah'
        verbose_name_plural = 'Enrolmen Sekolah'
    
    def __str__(self):
        return f"{self.school} - {self.year} - {self.average}"
    
class Contact_us(models.Model):
    name = models.CharField(max_length=200, verbose_name='nama') 
    email = models.EmailField()
    message = models.CharField(max_length=300, verbose_name='mesej')

    class Meta:
        verbose_name = 'Maklum Balas'
        verbose_name_plural = 'Maklum Balas'
    def __str__(self):
        return f"{self.name} - {self.message}"

