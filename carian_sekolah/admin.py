# dalam carian_sekolah/admin.py

from django.contrib.gis import admin
from django.utils.html import format_html
from .models import School, SchoolImageSubmission
from leaflet.admin import LeafletGeoAdmin


@admin.register(School)
class SchoolAdmin(admin.GISModelAdmin):
    # Baris ini adalah yang paling penting untuk membetulkan ralat
    gis_widget_kwargs = {
        "attrs": {
            "default_zoom": 11,
            "default_lat": 3.0449,
            "default_lon": 101.4456,
        },
    }

    list_display = ("name", "address")
    search_fields = ("name", "address")

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
            # Pautan ke gambar untuk dilihat dalam saiz penuh
            return format_html(
                '<a href="{0}" target="_blank"><img src="{0}" width="100" /></a>',
                obj.image.url,
            )
        return "Tiada Gambar"

    image_thumbnail.short_description = "Pralihat Gambar"

    @admin.action(description="Luluskan gambar yang dipilih & jadikan gambar utama")
    def approve_images(self, request, queryset):
        for submission in queryset:
            # Kemas kini gambar utama sekolah
            school = submission.school
            school.photo = submission.image
            school.save()

            # Kemas kini status serahan ini
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
