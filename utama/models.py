from django.db import models
from django.core.validators import RegexValidator


# Maklumat pilihan sekolah mengikut tahun
class TahunModel(models.Model):
    YEAR_CHOICES = [
        ("PPKI", "PPKI"),
        ("TAHUN SATU", "TAHUN 1"),
        ("TAHUN DUA", "TAHUN 2"),
        ("TAHUN TIGA", "TAHUN 3"),
        ("TAHUN EMPAT", "TAHUN 4"),
        ("TAHUN LIMA", "TAHUN 5"),
        ("TAHUN ENAM", "TAHUN 6"),
    ]
    tahun = models.CharField(
        max_length=11,
        default="TAHUN 1",
        choices=YEAR_CHOICES,
        verbose_name="Tingkatan Tahun",
    )

    class Meta:
        verbose_name = "Tahun"
        verbose_name_plural = "Tahun"
        ordering = ["tahun"]

    def __str__(self):
        return self.tahun


choices = TahunModel.YEAR_CHOICES


# Maklumat info Pelajar
class Info(models.Model):
    name = models.CharField(max_length=150, null=True, blank=False, verbose_name="Nama")
    phone_no_regex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    no_tel = models.CharField(
        validators=[phone_no_regex],
        max_length=16,
        unique=True,
        verbose_name="Nombor Telefon",
    )
    no_ic = models.CharField(max_length=12, verbose_name="No. MYKID")
    email = models.EmailField(max_length=255, verbose_name="E-Mail")
    jum_kelas = models.IntegerField(default=0, verbose_name="jumlah kelas")
    jum_murid = models.IntegerField(default=0, verbose_name="Jumlah Murid")

    list_sek = models.ForeignKey(
        "ListSekolah",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Senarai Sekolah",
        related_name="info_list_sekolah",
    )

    tahun = models.ForeignKey(
        "TahunModel",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Tahun",
    )

    list_kod_sekolah = models.ForeignKey(
        "ListSekolah",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="info_list_kod_sekolah",
    )
    purata = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Info"
        verbose_name_plural = "Info"

    def __str__(self):
        return f"{self.name}-{self.no_ic}"


# Nama Sekolah dan kod sekolah.
class ListSekolah(models.Model):
    nama_sek = models.CharField(max_length=255, verbose_name="Nama Sekolah")
    kod_sekolah = models.CharField(max_length=8)

    class Meta:
        verbose_name = "Senarai Sekolah"
        verbose_name_plural = "Senarai Sekolah"

    def __str__(self):
        return self.nama_sek
