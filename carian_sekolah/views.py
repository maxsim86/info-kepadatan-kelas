import requests
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.core.cache import cache
from django.db.models import Q
from .models import School
from .forms import ImageSubmissionForm 

# Konfigurasi Google Maps API (Jika ada)
GOOGLE_API_KEY = None 

def paparan_pencari(request):
    """
    View untuk memaparkan halaman utama pencari sekolah.
    """
    return render(request, 'carian_sekolah/pencari.html', {})

def find_school_in_db(query):
    """
    Cuba cari sekolah dalam DB berdasarkan nama.
    Pulangkan lat/lon jika jumpa.
    """
    # Cari sekolah yang namanya hampir sama (case-insensitive)
    school = School.objects.filter(name__icontains=query).first()
    if school and school.location:
        return school.location.y, school.location.x, school.name
    return None, None, None

def get_coordinates(query):
    """
    Fungsi pembantu untuk mendapatkan koordinat (Geocoding).
    Prioriti: DB (Nama Sekolah) -> Cache -> Google -> Photon -> Nominatim.
    """
    # 1. Semak jika input adalah nama sekolah dalam DB (Paling Pantas)
    lat, lon, name = find_school_in_db(query)
    if lat and lon:
        return lat, lon, name

    # 2. Opsyen Google Maps
    if GOOGLE_API_KEY:
        try:
            url = f"https://maps.googleapis.com/maps/api/geocode/json?address={query},+Malaysia&key={GOOGLE_API_KEY}"
            response = requests.get(url, timeout=3)
            data = response.json()
            if data['status'] == 'OK':
                loc = data['results'][0]['geometry']['location']
                return float(loc['lat']), float(loc['lng']), data['results'][0]['formatted_address']
        except Exception:
            pass

    # 3. Opsyen Photon (Komoot) - Pantas & Percuma
    try:
        url = f"https://photon.komoot.io/api/?q={query}&limit=1&lang=en"
        response = requests.get(url, timeout=3)
        data = response.json()
        if data['features']:
            coords = data['features'][0]['geometry']['coordinates']
            props = data['features'][0]['properties']
            display_name = f"{props.get('name', '')} {props.get('street', '')}, {props.get('city', '')}"
            return float(coords[1]), float(coords[0]), display_name
    except Exception:
        pass

    # 4. Opsyen Nominatim (Fallback Terakhir)
    try:
        headers = {'User-Agent': 'SchoolLocatorApp/1.0'}
        url = f"https://nominatim.openstreetmap.org/search?format=json&q={query}, Malaysia&limit=1"
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon']), data[0]['display_name']
    except Exception:
        pass

    return None, None, None

def search_and_find_schools(request):
    """
    API endpoint untuk carian HTMX.
    """
    location_query = request.GET.get('location', '').strip()
    try:
        radius_km = float(request.GET.get('radius', 5.0))
    except ValueError:
        radius_km = 5.0
    
    # 1. Semak jika Lat/Lon dihantar terus (Dari butang GPS atau Autocomplete)
    param_lat = request.GET.get('lat')
    param_lon = request.GET.get('lon')
    
    user_lat = None
    user_lon = None

    if param_lat and param_lon:
        try:
            user_lat = float(param_lat)
            user_lon = float(param_lon)
        except ValueError:
            pass 

    # 2. Jika tiada Lat/Lon, lakukan Geocoding Pintar
    if user_lat is None or user_lon is None:
        if not location_query:
            return HttpResponse("<div class='alert alert-warning'>Sila masukkan lokasi atau pilih dari senarai.</div>")

        # Cuba cache
        cache_key = f"geo_v2_{location_query.lower().replace(' ', '')}"
        cached_coords = cache.get(cache_key)

        if cached_coords:
            user_lat, user_lon = cached_coords
        else:
            user_lat, user_lon, _ = get_coordinates(location_query)
            
            if user_lat is None:
                return HttpResponse(f"<div class='alert alert-danger'>Lokasi '{location_query}' tidak ditemui. Cuba poskod.</div>")
            
            # Simpan cache 24 jam
            cache.set(cache_key, (user_lat, user_lon), 60 * 60 * 24)

    # --- 3. Carian GeoDjango (Proximity Search) ---
    user_point = Point(user_lon, user_lat, srid=4326)

    # Optimasi: Guna .defer() untuk tidak memuatkan field berat jika tidak perlu
    # atau .only() untuk ambil yang perlu sahaja.
    nearby_schools = School.objects.filter(
        location__distance_lte=(user_point, D(km=radius_km))
    ).annotate(
        distance=Distance('location', user_point)
    ).order_by('distance')

    # --- 4. Sediakan Data JSON untuk Peta ---
    map_data_schools = []
    # Kita iterate queryset sekali sahaja untuk template DAN map data
    # (Django querysets are lazy/cached once evaluated)
    
    for school in nearby_schools:
        photo_url = school.photo.url if school.photo else None
        map_data_schools.append({
            'name': school.name,
            'lat': school.location.y,
            'lon': school.location.x,
            'photo_url': photo_url,
            'distance': round(school.distance.km, 2)
        })

    trigger_data = {
        'search_location': {'lat': user_lat, 'lon': user_lon},
        'schools': map_data_schools
    }

    context = {
        'schools': nearby_schools,
        'search_location': location_query or "Lokasi GPS",
        'radius': radius_km
    }
    html = render_to_string('carian_sekolah/partials/results_list.html', context)
    
    response = HttpResponse(html)
    response['HX-Trigger'] = json.dumps({'updateMap': trigger_data})
    
    return response

def address_autocomplete(request):
    """
    API Autocomplete menggunakan Photon.
    """
    query = request.GET.get("location", "").strip()
    suggestions = []
    
    if len(query) > 2:
        cache_key = f"auto_photon_{query.lower().replace(' ', '')}"
        suggestions = cache.get(cache_key)

        if not suggestions:
            suggestions = []  # Initialize as empty list if cache miss
            
            # 1. Cari Sekolah dalam DB dulu (Supaya user boleh cari nama sekolah terus)
            db_schools = School.objects.filter(name__icontains=query)[:3]
            for school in db_schools:
                if school.location:
                    suggestions.append({
                        "display_name": f"{school.name} (Sekolah)",
                        "lat": school.location.y,
                        "lon": school.location.x
                    })

            # 2. Cari Alamat guna Photon
            url = f"https://photon.komoot.io/api/?q={query}&limit=5&lang=en"
            try:
                response = requests.get(url, timeout=2)
                if response.status_code == 200:
                    data = response.json()
                    for feature in data['features']:
                        props = feature['properties']
                        parts = [
                            props.get('name'), props.get('street'),
                            props.get('city'), props.get('state')
                        ]
                        display_name = ", ".join([p for p in parts if p])
                        coords = feature['geometry']['coordinates']
                        
                        suggestions.append({
                            "display_name": display_name,
                            "lat": coords[1],
                            "lon": coords[0]
                        })
                
                if suggestions: # Only cache if we found something
                    cache.set(cache_key, suggestions, 60 * 60) # Cache 1 jam
            except Exception:
                pass

    return render(
        request,
        "carian_sekolah/partials/autocomplete_results.html",
        {"suggestions": suggestions},
    )

def submit_school_image(request, school_id):
    school = get_object_or_404(School, id=school_id)
    if request.method == "POST":
        form = ImageSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.school = school
            submission.save()
            return redirect("carian_sekolah:submission_thank_you")
    else:
        form = ImageSubmissionForm()
    return render(
        request, "carian_sekolah/submit_image.html", {"school": school, "form": form}
    )

def submission_thank_you(request):
    return render(request, "carian_sekolah/submission_thank_you.html")