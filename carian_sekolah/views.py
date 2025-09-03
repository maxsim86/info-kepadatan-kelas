import requests
import json
from django.shortcuts import render
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models import Q # Pastikan Q diimport
from .models import School
from django.contrib.gis.db.models.functions import Distance
from django.core.cache import cache
from django.contrib.postgres.search import SearchVector, SearchQuery

def paparan_pencari(request):
    return render(request, 'carian_sekolah/pencari.html', {})

def search_and_find_schools(request):
    location_query = request.GET.get('location', '').strip()
    school_type = request.GET.get('type', 'SEMUA').upper()
    radius_km = float(request.GET.get('radius', 3.0))

    if not location_query:
        return HttpResponse("<div class='list-group-item text-danger'>Sila masukkan nama sekolah atau lokasi.</div>")

    # === LOGIK CARIAN HIBRID ===

    # 1. Carian terus berdasarkan nama atau alamat dalam pangkalan data
    direct_matches_query = School.objects.annotate(
    search=SearchVector('name', 'address'),
).filter(search=SearchQuery(location_query))

    geocoded_matches_query = School.objects.none()
    search_location = None
    geocoding_failed = False
    
    # 2a. Semak cache dahulu
    cache_key = f"geodata_{location_query.lower()}"
    cached_location = cache.get(cache_key)

    if cached_location:
        search_location = cached_location
        geodata_found = True
    else:
        # 2b. Jika tiada dalam cache, baru buat panggilan API
        geodata_found = False
        nominatim_url = f"https://nominatim.openstreetmap.org/search?format=json&q={location_query}, Malaysia"
        try:
            response = requests.get(nominatim_url, headers={'User-Agent': 'SchoolLocatorApp/1.0'})
            response.raise_for_status()
            geodata = response.json()
            if geodata:
                lat = float(geodata[0]['lat'])
                lon = float(geodata[0]['lon'])
                search_location = {'lat': lat, 'lon': lon}
                # 2c. Simpan hasil dalam cache selama 1 hari (86400 saat)
                cache.set(cache_key, search_location, 86400)
                geodata_found = True
        except (requests.RequestException, IndexError, KeyError):
            pass # Gagal secara senyap

    if geodata_found:
        user_location_point = Point(search_location['lon'], search_location['lat'], srid=4326)
        geocoded_matches_query = School.objects.filter(
            location__distance_lte=(user_location_point, D(km=radius_km))
        )
    else:
        geocoding_failed = True

    # 3. Gabungkan kedua-dua hasil carian dan buang yang berulang
    combined_query = (direct_matches_query | geocoded_matches_query).distinct()

    # 4. Gunakan penapis jenis sekolah pada hasil yang telah digabungkan
    if school_type in ['RENDAH', 'MENENGAH']:
        combined_query = combined_query.filter(school_type=school_type)

    # 5. Anotasi jarak (jika lokasi ditemui) dan susun
    if search_location:
        user_location_point = Point(search_location['lon'], search_location['lat'], srid=4326)
        final_query = combined_query.annotate(
            distance=Distance('location', user_location_point)
        ).order_by('distance')
    else:
        # Jika lokasi tidak dapat dikesan, susun mengikut nama sahaja
        final_query = combined_query.order_by('name')

    # Sediakan data untuk frontend
    results_for_js = []
    for school_obj in final_query:
        results_for_js.append({
            'name': school_obj.name,
            'lat': school_obj.location.y,
            'lon': school_obj.location.x,
        })
        
    context = {
        'schools': final_query, 
        'search_location_found': bool(search_location),
        'geocoding_failed': geocoding_failed,
        'location_query': location_query
    }
    html = render_to_string('carian_sekolah/partials/results_list.html', context, request)
    
    trigger_data = {
        'search_location': search_location,
        'schools': results_for_js
    }
    response = HttpResponse(html)
    response['HX-Trigger'] = json.dumps({'updateMap': trigger_data})
    
    return response

