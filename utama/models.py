from django.db import models

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
    year = models.CharField(max_length=10, choices= YEAR_CHOICES)
    average = models.IntegerField()
    
    def __str__(self):
        return f"{self.school} - {self.average} - {self.year}"
    
class Contact_us(models.Model):
    name = models.CharField(max_length=200) 
    email = models.EmailField()
    message = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.name} - {self.message}"