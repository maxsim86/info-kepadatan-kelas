from django.contrib.gis import admin
from django.utils.html import format_html
from .models import School, SchoolImageSubmission
from leaflet.admin import LeafletGeoAdmin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin

# === RESOURCE: Konfigurasi Import/Export ===
class SchoolResource(resources.ModelResource):
    # Cipta field maya untuk lat/lon supaya mudah dibaca dalam CSV/Excel
    latitude = fields.Field(column_name='latitude', attribute='latitude')
    longitude = fields.Field(column_name='longitude', attribute='longitude')

    class Meta:
        model = School
        # Gunakan kod_sekolah sebagai ID unik (untuk update data sedia ada)
        import_id_fields = ('kod_sekolah',)
        # Senarai lajur yang akan muncul dalam fail Excel/CSV
        fields = ('kod_sekolah', 'name', 'ppd', 'address', 'postcode', 'school_type', 'latitude', 'longitude', 'location')
        # Susunan lajur
        export_order = ('kod_sekolah', 'name', 'address', 'postcode', 'ppd', 'school_type', 'latitude', 'longitude')
        
        # === OPTIMASI IMPORT FAIL BESAR ===
        skip_unchanged = True       # Jangan proses baris yang tiada perubahan
        report_skipped = False      # Jangan penuhi log dengan baris yang diskip
        use_bulk = True             # Guna bulk create/update untuk kelajuan

    # --- LOGIK EXPORT (Database -> CSV) ---
    def dehydrate_latitude(self, school):
        # Ambil nilai Y (Latitud) dari PointField jika wujud
        if school.location:
            return school.location.y
        return ''

    def dehydrate_longitude(self, school):
        # Ambil nilai X (Longitud) dari PointField jika wujud
        if school.location:
            return school.location.x
        return ''

    # --- LOGIK IMPORT (CSV -> Database) ---
    def before_import_row(self, row, **kwargs):
        """
        Gabungkan lat/lon menjadi PointField sebelum simpan
        """
        lat = row.get('latitude')
        lon = row.get('longitude')
        
        if lat and lon:
            try:
                # Format WKT: POINT(longitude latitude)
                row['location'] = f"POINT({lon} {lat})"
            except Exception as e:
                pass

# === ADMIN ===
@admin.register(School)
# PEMBETULAN UTAMA: Tambah ImportExportModelAdmin DI SINI
class SchoolAdmin(ImportExportModelAdmin, LeafletGeoAdmin):
    resource_class = SchoolResource
    
    # Tetapan Widget Peta Leaflet
    settings_overrides = {
        'DEFAULT_CENTER': (3.0449, 101.4456), # Pusat Peta (Klang)
        'DEFAULT_ZOOM': 10,
    }

    list_display = ("name", "ppd", "school_type", "kod_sekolah")
    search_fields = ("name", "address", "kod_sekolah")
    list_filter = ("school_type", "ppd")
    list_per_page = 500

@admin.register(SchoolImageSubmission)
class SchoolImageSubmissionAdmin(admin.ModelAdmin):
    list_display = ("school", "image_thumbnail", "status", "uploaded_at")
    list_filter = ("status", "school__ppd")
    search_fields = ("school__name",)
    list_per_page = 20

    actions = ["approve_images", "reject_images"]

    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<a href="{0}" target="_blank"><img src="{0}" width="100" /></a>',
                obj.image.url,
            )
        return "Tiada Gambar"

    image_thumbnail.short_description = "Pralihat Gambar"

    @admin.action(description="Luluskan gambar yang dipilih & jadikan gambar utama")
    def approve_images(self, request, queryset):
        for submission in queryset:
            school = submission.school
            school.photo = submission.image
            school.save()
            submission.status = SchoolImageSubmission.StatusChoices.APPROVED
            submission.save()

        self.message_user(
            request,
            f"{queryset.count()} gambar telah diluluskan dan ditetapkan sebagai gambar utama.",
        )

    @admin.action(description="Tolak gambar yang dipilih")
    def reject_images(self, request, queryset):
        queryset.update(status=SchoolImageSubmission.StatusChoices.REJECTED)
        self.message_user(request, f"{queryset.count()} gambar telah ditolak.")