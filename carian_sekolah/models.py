from django.db import models
from django.contrib.gis.db import models as gis_models


class Name(models.Model):
    class SchoolType(models.TextChoices):
        RENDAH = "RENDAH", "Sekolah Rendah"
        MENENGAH = "MENENGAH", "Sekolah Menengah"
    kod_sekolah = models.CharField(
        max_length=10, unique=True, verbose_name="kod sekolah", null=True, blank=True
    )

class School(models.Model):
    class SchoolType(models.TextChoices):
        RENDAH = "RENDAH", "Sekolah Rendah"
        MENENGAH = "MENENGAH", "Sekolah Menengah"

    kod_sekolah = models.CharField(
        max_length=10, unique=True, verbose_name="Kod Sekolah", null=True, blank=True
    )
    ppd = models.CharField(max_length=100, verbose_name="PPD", null=True, blank=True)
    name = models.CharField(max_length=255, verbose_name="Nama Sekolah")
    address = models.TextField(verbose_name="Alamat Penuh", blank=True)
    postcode = models.CharField(
        max_length=10, verbose_name="Poskod", blank=True, null=True
    )
    school_type = models.CharField(
        max_length=10,
        choices=SchoolType.choices,
        default=SchoolType.RENDAH,
        verbose_name="Jenis Sekolah",
    )
    db_index = True

    #hanya mencari satu lokasi sahaja
    location = gis_models.PointField(verbose_name="Koordinat Lokasi")

    photo = models.ImageField(
        upload_to="school_photos/",
        null=True,
        blank=True,
        verbose_name="Gambar Utama Sekolah",
    )

    class Meta:
        verbose_name = "Sekolah"
        verbose_name_plural = "Senarai Sekolah"

    def __str__(self):
        return self.name


class SchoolImageSubmission(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "PENDING", "Menunggu Kelulusan"
        APPROVED = "APPROVED", "Diluluskan"
        REJECTED = "REJECTED", "Ditolak"

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,related_name="submissions",verbose_name="sekolah",)
    image = models.ImageField(
        upload_to="submissions/", verbose_name="Gambar yang dimuat naik"
    )
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        verbose_name="status",
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Tarikh dimuat naik"
    )

    class Meta:
        verbose_name = "Serahan Gambar Sekolah"
        verbose_name_plural = "Serahan Gambar Sekolah"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"Serahan untuk {self.school.name} ({self.status})"


