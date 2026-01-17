from django.db import models
from django.contrib.gis.db import models as gis_models

# Class 'Name' yang lama telah dibuang kerana kelihatan tidak digunakan/duplikasi.

class School(models.Model):
    # === KEMAS KINI DI SINI: Senarai Pilihan Baru ===
    class SchoolType(models.TextChoices):
        SK = "SK", "Sekolah Kebangsaan (SK)"
        SJKC = "SJK(C)", "SJK Cina"
        SJKT = "SJK(T)", "SJK Tamil"
        SMK = "SMK", "Sekolah Menengah Kebangsaan"
        SMJK = "SMJK", "Sekolah Menengah Jenis Kebangsaan"
        SABK = "SM Agama (SABK)", "SM Agama (SABK)"
        SMK_Agama = "SMK Agama", "Sekolah Menengah Kebangsaan Agama MAAHAD"
        KOLEJ = "Kolej Tingkatan 6", "Kolej Tingkatan 6"
        KV = "KV", "Kolej Vokasional"
        SMBP = "SMBP", "SM Berasrama Penuh"
        SK_ASLI ="SK (Asli)","SK Asli"
        LAIN = "LAIN", "Lain-lain"

    kod_sekolah = models.CharField(
        max_length=10, 
        unique=True, 
        verbose_name="Kod Sekolah", 
        null=True, 
        blank=True,
        db_index=True
    )
    name = models.CharField(max_length=255, verbose_name="Nama Sekolah", db_index=True)
    address = models.TextField(verbose_name="Alamat Penuh", blank=True)
    
    ppd = models.CharField(max_length=100, verbose_name="PPD", null=True, blank=True, db_index=True)
    city = models.CharField(max_length=100, verbose_name="Bandar", null=True, blank=True, db_index=True)
    postcode = models.CharField(max_length=30, verbose_name="Poskod", blank=True, null=True, db_index=True)
    
    # === GUNAKAN PILIHAN DI SINI ===
    school_type = models.CharField(
        max_length=50,
        choices=SchoolType.choices, # Sambungkan pilihan di sini
        default=SchoolType.SK,
        verbose_name="Jenis Sekolah",
        db_index=True
    )

    location = gis_models.PointField(
        verbose_name="Koordinat Lokasi", 
        srid=4326, 
        geography=True,
        help_text="Format automatik dari sistem GPS"
    )

    photo = models.ImageField(
        upload_to="school_photos/",
        null=True,
        blank=True,
        verbose_name="Gambar Utama Sekolah",
    )

    class Meta:
        verbose_name = "Sekolah"
        verbose_name_plural = "Senarai Sekolah"
        ordering = ['name']

    def __str__(self):
        return f"{self.kod_sekolah} - {self.name}"

    @property
    def latitude(self):
        return self.location.y if self.location else None

    @property
    def longitude(self):
        return self.location.x if self.location else None


class SchoolImageSubmission(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "PENDING", "Menunggu Kelulusan"
        APPROVED = "APPROVED", "Diluluskan"
        REJECTED = "REJECTED", "Ditolak"

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="submissions",
        verbose_name="Sekolah",
    )
    image = models.ImageField(
        upload_to="submissions/", 
        verbose_name="Gambar yang dimuat naik"
    )
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        verbose_name="Status Kelulusan",
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Tarikh dimuat naik"
    )

    class Meta:
        verbose_name = "Serahan Gambar"
        verbose_name_plural = "Senarai Serahan Gambar"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.school.name} - {self.get_status_display()}"