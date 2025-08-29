# carian_sekolah/views.py

import requests
import json
from django.shortcuts import render
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import School
from django.contrib.gis.db.models.functions import Distance

def paparan_pencari(request):
    """
    Memaparkan halaman utama untuk aplikasi pencari sekolah.
    """
    return render(request, 'carian_sekolah/pencari.html', {})

def search_and_find_schools(request):
    """
    View ini mengendalikan permintaan HTMX:
    1. Menerima input lokasi (teks) dari pengguna.
    2. Menukar teks lokasi kepada koordinat (Geocoding).
    3. Mencari sekolah berdekatan dalam pangkalan data (Proximity Search).
    4. Memulangkan senarai sekolah (HTML) dan data peta (header HX-Trigger).
    """
    location_query = request.GET.get('location', '')
    school_type = request.GET.get('type', 'RENDAH')
    radius_km = float(request.GET.get('radius', 3.0))

    # Baris yang menyebabkan ralat telah dibuang dari sini.

    if not location_query:
        return HttpResponse("<div class='list-group-item text-danger'>Sila masukkan lokasi.</div>")

    # Langkah 1: Geocode alamat menggunakan Nominatim
    nominatim_url = f"https://nominatim.openstreetmap.org/search?format=json&q={location_query}, Selangor, Malaysia"
    try:
        response = requests.get(nominatim_url, headers={'User-Agent': 'SchoolLocatorApp/1.0'})
        response.raise_for_status()
        geodata = response.json()
        if not geodata:
            return HttpResponse("<div class='list-group-item text-danger'>Lokasi tidak ditemui.</div>")
        
        lat = float(geodata[0]['lat'])
        lon = float(geodata[0]['lon'])
    except requests.RequestException:
        return HttpResponse("<div class='list-group-item text-danger'>Ralat semasa menghubungi servis geocoding.</div>")
    except (IndexError, KeyError):
         return HttpResponse("<div class='list-group-item text-danger'>Data lokasi tidak lengkap diterima.</div>")

    # Langkah 2: Lakukan carian jarak menggunakan GeoDjango
    user_location = Point(lon, lat, srid=4326) # SRID yang betul digunakan di sini
    nearby_schools_query = School.objects.filter(
        school_type=school_type,
        location__distance_lte=(user_location, D(km=radius_km))
    ).annotate(
        distance=Distance('location', user_location)
    ).order_by('distance')

    # Langkah 3: Sediakan data untuk frontend (diperkemas)
    results_for_js = []
    for school_obj in nearby_schools_query:
        results_for_js.append({
            'name': school_obj.name,
            'lat': school_obj.location.y,
            'lon': school_obj.location.x,
        })

    # Hantar keseluruhan queryset yang telah disusun ke templat
    context = {'schools': nearby_schools_query}
    html = render_to_string('carian_sekolah/partials/results_list.html', context)
    
    # Langkah 4: Cipta header HX-Trigger dengan data untuk peta
    trigger_data = {
        'search_location': {'lat': lat, 'lon': lon},
        'schools': results_for_js
    }
    
    response = HttpResponse(html)
    response['HX-Trigger'] = json.dumps({'updateMap': trigger_data})
    
    return response