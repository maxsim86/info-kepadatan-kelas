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

    school = models.CharField(max_length=50, choices=SCHOOL_CHOICES)
    year = models.CharField(max_length=10, choices= YEAR_CHOICES)
    purata = models.IntegerField()
    
    def __str__(self):
        return f"{self.school} - {self.purata} - {self.year}"
    
    