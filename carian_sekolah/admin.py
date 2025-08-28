# dalam carian_sekolah/admin.py

from django.contrib.gis import admin
from .models import School

@admin.register(School)
class SchoolAdmin(admin.GISModelAdmin):
    gis_widget_kwargs = {
        "attrs": {
            "default_zoom": 11,
            "default_lat": 3.0449,
            "default_lon": 101.4456,
        },
    }
    list_display = ('name', 'address')
    search_fields = ('name', 'address')