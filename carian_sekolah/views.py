import requests
import json
import re
from django.shortcuts import render
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models import Q
from .models import School
from django.contrib.gis.db.models.functions import Distance
from django.core.cache import cache
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

def paparan_pencari(request):
    return render(request, 'carian_sekolah/pencari.html', {})

def geocode_location(location_query):
    """
    Fungsi ini menukar teks lokasi kepada koordinat.
    Ia kini mempunyai logik sandaran (fallback) dan caching.
    """
    cache_key = f"geodata_{location_query.lower().replace(' ', '_')}"
    cached_location = cache.get(cache_key)
    if cached_location:
        return cached_location, location_query

    search_queries = [location_query]
    postcode_match = re.search(r'\b\d{5}\b', location_query)
    if postcode_match:
        search_queries.append(postcode_match.group(0))

    for query in search_queries:
        nominatim_url = f"https://nominatim.openstreetmap.org/search?format=json&q={query}, Malaysia"
        try:
            response = requests.get(nominatim_url, headers={'User-Agent': 'SchoolLocatorApp/1.0'})
            response.raise_for_status()
            geodata = response.json()
            if geodata:
                lat = float(geodata[0]['lat'])
                lon = float(geodata[0]['lon'])
                search_location = {'lat': lat, 'lon': lon}
                cache.set(cache_key, search_location, 86400) # Simpan dalam cache selama 1 hari
                return search_location, query
        except (requests.RequestException, IndexError, KeyError):
            continue
            
    return None, location_query

def search_and_find_schools(request):
    location_query = request.GET.get('location', '').strip()
    school_type = request.GET.get('type', 'SEMUA').upper()
    radius_km = float(request.GET.get('radius', 3.0))

    if not location_query:
        return HttpResponse("<div class='list-group-item text-danger'>Sila masukkan nama sekolah atau lokasi.</div>")

    # 1. Carian terus berdasarkan nama, alamat, dan poskod
    vector = SearchVector('name', 'address')
    search_query = SearchQuery(location_query)
    direct_matches_query = School.objects.annotate(
        rank=SearchRank(vector, search_query)
    ).filter(rank__gte=0.01)

    # 2. Carian Geografi dengan Logik Sandaran
    search_location, successful_query = geocode_location(location_query)
    geocoded_matches_query = School.objects.none()
    
    if search_location:
        user_location_point = Point(search_location['lon'], search_location['lat'], srid=4326)
        # Ambil semua sekolah dalam radius yang lebih besar sedikit sebagai calon awal
        # Ini penting supaya carian teks tidak terlepas
        geocoded_matches_query = School.objects.filter(
            location__distance_lte=(user_location_point, D(km=radius_km + 5)) # Cth: radius + 5km
        )

    # 3. Gabungkan hasil carian
    combined_query = (direct_matches_query | geocoded_matches_query).distinct()
    if school_type in ['RENDAH', 'MENENGAH']:
        combined_query = combined_query.filter(school_type=school_type)

    # 4. Anotasi jarak dan susun hasil
    if search_location:
        user_location_point = Point(search_location['lon'], search_location['lat'], srid=4326)
        
        # === PERUBAHAN UTAMA DI SINI ===
        # Tapis sekali lagi pada hasil yang digabungkan untuk memastikan SEMUA hasil
        # mematuhi radius yang ditetapkan oleh pengguna.
        final_query = combined_query.annotate(
            distance=Distance('location', user_location_point)
        ).filter(
            distance__lte=D(km=radius_km)
        ).order_by('distance')
        # === TAMAT PERUBAHAN ===
    else:
        # Jika lokasi tidak dapat dikesan, susun mengikut nama sahaja
        final_query = combined_query.order_by('name')

    # 5. Sediakan data untuk frontend
    results_for_js = []
    for school_obj in final_query:
        results_for_js.append({'name': school_obj.name, 'lat': school_obj.location.y, 'lon': school_obj.location.x})
        
    context = {
        'schools': final_query, 
        'search_location_found': bool(search_location),
        'geocoding_failed': not bool(search_location),
        'location_query': location_query,
        'successful_query': successful_query if not bool(search_location) and successful_query != location_query else None
    }
    html = render_to_string('carian_sekolah/partials/results_list.html', context)
    
    trigger_data = {'search_location': search_location, 'schools': results_for_js}
    response = HttpResponse(html)
    response['HX-Trigger'] = json.dumps({'updateMap': trigger_data})
    
    return response