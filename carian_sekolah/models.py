from django.db import models
from django.contrib.gis.db import models as gis_models

# Create your models here.
class School(models.Model):
    """
    Model ini mewakili satu entiti sekolah dengan lokasi geografinya.
    Ia menggunakan PointField dari GeoDjango untuk menyimpan koordinat.
    """
    
    class SchoolType(models.TextChoices):
        RENDAH = 'RENDAH', 'Sekolah Rendah'
        MENENGAH = 'MENENGAH', 'Sekolah Menengah'
        
    kod_sekolah = models.CharField(
        max_length=10, 
        unique=True,  # Kod sekolah sepatutnya unik
        verbose_name="Kod Sekolah", null=True, blank=True
    )
    ppd = models.CharField(
        max_length=100, 
        verbose_name="PPD",
        null=True,blank=True
    )
    
    # Medan standard untuk menyimpan maklumat asas sekolah.
    name = models.CharField(
        max_length=255, 
        verbose_name="Nama Sekolah"
    )
    address = models.TextField(
        verbose_name="Alamat Penuh",
        blank=True # Alamat boleh dikosongkan jika tidak diketahui.
    )
    location = gis_models.PointField(
        verbose_name="Koordinat Lokasi"
    )

    school_type = models.CharField(
        max_length=10,
        choices=SchoolType.choices,
        default=SchoolType.RENDAH,
        verbose_name="Jenis Sekolah"
    )


    class Meta:
        verbose_name = "Sekolah"
        verbose_name_plural = "Senarai Sekolah"

    def __str__(self):
        """
        Mengembalikan representasi string untuk model ini, 
        yang akan digunakan di antaramuka admin.
        """
        return self.name

