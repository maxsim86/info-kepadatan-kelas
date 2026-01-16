import requests
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.core.cache import cache
from .models import School
from .forms import ImageSubmissionForm 

# Konfigurasi Google Maps API (Jika anda ada API Key pada masa depan)
GOOGLE_API_KEY = None  # Letak API Key anda di sini: 'AIzaSy...'

def paparan_pencari(request):
    """
    View untuk memaparkan halaman utama pencari sekolah.
    """
    return render(request, 'carian_sekolah/pencari.html', {})

def get_coordinates(query):
    """
    Fungsi pembantu untuk mendapatkan koordinat.
    Boleh ditukar antara Nominatim, Photon, atau Google Maps.
    """
    # Opsyen 1: Google Maps (Paling Tepat - Jika ada Key)
    if GOOGLE_API_KEY:
        try:
            url = f"https://maps.googleapis.com/maps/api/geocode/json?address={query},+Malaysia&key={GOOGLE_API_KEY}"
            response = requests.get(url, timeout=5)
            data = response.json()
            if data['status'] == 'OK':
                loc = data['results'][0]['geometry']['location']
                return float(loc['lat']), float(loc['lng']), data['results'][0]['formatted_address']
        except Exception:
            pass # Fallback ke provider lain jika gagal

    # Opsyen 2: Photon (Komoot) - Lebih pantas & lenient untuk carian teks bebas
    try:
        # Photon fokus pada carian lokasi, sangat pantas
        url = f"https://photon.komoot.io/api/?q={query}&limit=1"
        response = requests.get(url, timeout=5)
        data = response.json()
        if data['features']:
            coords = data['features'][0]['geometry']['coordinates']
            props = data['features'][0]['properties']
            
            # Bina nama paparan ringkas
            display_name = f"{props.get('name', '')} {props.get('street', '')}, {props.get('city', '')}"
            
            # Photon memulangkan [lon, lat]
            return float(coords[1]), float(coords[0]), display_name
    except Exception:
        pass

    # Opsyen 3: Nominatim (Fallback Asal) - Bagus untuk alamat berstruktur
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
    radius_km = float(request.GET.get('radius', 5.0))
    
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

    # 2. Jika tiada Lat/Lon, lakukan Geocoding (Guna fungsi pembantu baru)
    if user_lat is None or user_lon is None:
        if not location_query:
            return HttpResponse("<div class='alert alert-warning'>Sila masukkan lokasi atau pilih dari senarai.</div>")

        cache_key = f"geo_{location_query.lower().replace(' ', '')}"
        cached_coords = cache.get(cache_key)

        if cached_coords:
            user_lat, user_lon = cached_coords
        else:
            user_lat, user_lon, _ = get_coordinates(location_query)
            
            if user_lat is None:
                return HttpResponse(f"<div class='alert alert-danger'>Lokasi '{location_query}' tidak ditemui. Cuba poskod.</div>")
            
            # Simpan dalam cache
            cache.set(cache_key, (user_lat, user_lon), 60 * 60 * 24)

    # --- 3. Carian GeoDjango (Proximity Search) ---
    user_point = Point(user_lon, user_lat, srid=4326)

    nearby_schools = School.objects.filter(
        location__distance_lte=(user_point, D(km=radius_km))
    ).annotate(
        distance=Distance('location', user_point)
    ).order_by('distance')

    # --- 4. Sediakan Data JSON untuk Peta ---
    map_data_schools = []
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
        'search_location': location_query or "Koordinat Dipilih",
        'radius': radius_km
    }
    html = render_to_string('carian_sekolah/partials/results_list.html', context)
    
    response = HttpResponse(html)
    response['HX-Trigger'] = json.dumps({'updateMap': trigger_data})
    
    return response

def address_autocomplete(request):
    """
    API Autocomplete menggunakan Photon (Komoot) yang lebih pantas dan fleksibel.
    """
    query = request.GET.get("location", "").strip()
    suggestions = []
    
    if len(query) > 2:  # Photon boleh proses seawal 3 aksara
        cache_key = f"auto_photon_{query.lower().replace(' ', '')}"
        suggestions = cache.get(cache_key)

        if not suggestions:
            # Guna Photon API untuk autocomplete (Percuma & Tiada had ketat seperti Nominatim)
            # Kita tambah bias lokasi Malaysia (box approximate) atau lang code
            url = f"https://photon.komoot.io/api/?q={query}&limit=5&lang=en"
            
            try:
                response = requests.get(url, timeout=3)
                response.raise_for_status()
                data = response.json()
                
                suggestions = []
                for feature in data['features']:
                    props = feature['properties']
                    
                    # Tapis supaya logik sikit (utamakan yang ada bandar/negeri)
                    # Photon cari seluruh dunia, jadi kita cuba tapis jika boleh, 
                    # atau terima sahaja dan biar user pilih.
                    
                    # Format nama: Nama, Jalan, Bandar, Negara
                    parts = [
                        props.get('name'),
                        props.get('street'),
                        props.get('city') or props.get('town'),
                        props.get('state'),
                        props.get('country')
                    ]
                    display_name = ", ".join([p for p in parts if p])
                    
                    # Simpan koordinat supaya frontend tak perlu geocode lagi!
                    coords = feature['geometry']['coordinates'] # [lon, lat]
                    
                    suggestions.append({
                        "display_name": display_name,
                        "lat": coords[1],
                        "lon": coords[0]
                    })
                
                cache.set(cache_key, suggestions, 60 * 60)

            except (requests.RequestException, IndexError, KeyError):
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