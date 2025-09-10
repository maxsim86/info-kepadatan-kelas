# dalam carian_sekolah/admin.py

from django.contrib.gis import admin
from .models import School
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

    list_display = ('name', 'address')
    search_fields = ('name', 'address')
    
    list_per_page = 500
