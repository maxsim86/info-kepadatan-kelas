import requests
import json
import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from django.core.cache import cache
from .models import School
from .forms import ImageSubmissionForm 

# --- BAHAGIAN 1: PENGURUSAN GAMBAR ---

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

# --- BAHAGIAN 2: CARIAN & PETA ---

def paparan_pencari(request):
    """
    Memaparkan halaman utama pencari.
    """
    return render(request, 'carian_sekolah/pencari.html', {})

def address_autocomplete(request):
    """
    API untuk autocomplete alamat menggunakan PHOTON (Komoot).
    Lebih pantas & tiada had ketat seperti Nominatim.
    """
    query = request.GET.get("location", "").strip()
    suggestions = []
    
    if len(query) > 2:  
        # Fokus carian di Malaysia (Kod 'my')
        # Tambah User-Agent untuk elak 403 Forbidden
        headers = {'User-Agent': 'SchoolLocatorApp/1.0 (admin@example.com)'}
        
        # Encode query params
        params = {
            'q': query,
            'limit': 5,
            'lang': 'en',
            'lat': 3.0738, 
            'lon': 101.5183
        }
        
        try:
            response = requests.get("https://photon.komoot.io/api/", params=params, headers=headers, timeout=3)
            response.raise_for_status()
            data = response.json()
            
            for feature in data.get("features", []):
                props = feature.get("properties", {})
                
                # Bina alamat yang kemas dari komponen Photon
                name = props.get("name")
                street = props.get("street")
                housenumber = props.get("housenumber")
                city = props.get("city")
                state = props.get("state")
                country = props.get("country")
                
                parts = []
                if name: parts.append(name)
                if housenumber and street: 
                    parts.append(f"{housenumber} {street}")
                elif street and street != name: 
                    parts.append(street)
                
                if city: parts.append(city)
                if state: parts.append(state)
                
                # Hanya ambil lokasi di Malaysia
                if country == "Malaysia" or not country:
                    full_address = ", ".join(parts)
                    if full_address and full_address not in suggestions:
                        suggestions.append(full_address)

        except (requests.RequestException, IndexError, KeyError, ValueError) as e:
            # print(f"Autocomplete Error: {e}") # Boleh un-comment untuk debugging
            pass 

    return render(
        request,
        "carian_sekolah/partials/autocomplete_results.html",
        {"suggestions": suggestions},
    )

def normalize_school_name(query):
    query_upper = query.upper()
    query_upper = query_upper.replace("SEKOLAH KEBANGSAAN", "SK")
    query_upper = query_upper.replace("SEKOLAH MENENGAH KEBANGSAAN", "SMK")
    query_upper = query_upper.replace("SEKOLAH JENIS KEBANGSAAN", "SJK")
    return query_upper

def geocode_location_smart(query):
    """
    Fungsi pintar untuk mendapatkan koordinat menggunakan PHOTON.
    1. Semak Cache.
    2. Panggil Photon API.
    3. Fallback Poskod jika perlu.
    """
    query = query.strip()
    cache_key = f"geo_photon_{query.lower().replace(' ', '_')}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    def call_photon(q):
        try:
            headers = {'User-Agent': 'SchoolLocatorApp/1.0 (admin@example.com)'}
            params = {
                'q': q,
                'limit': 1,
                'lat': 4.2105, # Tengah Malaysia
                'lon': 101.9758
            }
            
            resp = requests.get("https://photon.komoot.io/api/", params=params, headers=headers, timeout=5)
            resp.raise_for_status()
            data = resp.json()
            
            features = data.get("features", [])
            if features:
                coords = features[0]["geometry"]["coordinates"]
                props = features[0]["properties"]
                
                # Pastikan result di Malaysia jika boleh
                if props.get("country") == "Malaysia" or not props.get("country"):
                    return {
                        'lat': float(coords[1]), # Photon guna [lon, lat]
                        'lon': float(coords[0]),
                        'display_name': props.get("name", q)
                    }
        except Exception as e:
            print(f"Photon Geocoding Error: {e}")
        return None

    # 1. Percubaan Utama
    result = call_photon(query)

    # 2. Fallback: Address Smoothing (Buang bahagian depan)
    if not result and "," in query:
        parts = query.split(",")
        while not result and len(parts) > 1:
            parts.pop(0) 
            broader_query = ",".join(parts).strip()
            if len(broader_query) > 3:
                result = call_photon(broader_query)

    # 3. Fallback: Poskod
    if not result:
        postcode_match = re.search(r'\b\d{5}\b', query)
        if postcode_match:
            result = call_photon(postcode_match.group(0))

    if result:
        cache.set(cache_key, result, 60 * 60 * 24) # Cache 24 jam

    return result

def search_and_find_schools(request):
    """
    Enjin Carian Pintar Hibrid (Kini menggunakan Photon).
    """
    location_query = request.GET.get('location', '').strip()
    school_type = request.GET.get('type', 'SEMUA')
    radius_input = request.GET.get('radius', '3')
    
    try:
        radius_km = float(radius_input)
    except ValueError:
        radius_km = 3.0

    if not location_query:
        return HttpResponse("<div class='p-3 text-muted text-center'>Sila masukkan lokasi atau nama sekolah.</div>")

    center_point = None
    search_source = "Unknown"
    lat, lon = None, None

    # === LANGKAH 1: CARIAN DATABASE (Local DB First) ===
    is_school_name = False
    upper_q = location_query.upper()
    if any(x in upper_q for x in ["SK ", "SMK ", "SJK", "SEKOLAH", "KOLEJ"]):
        is_school_name = True
    
    if is_school_name:
        normalized_query = normalize_school_name(location_query)
        local_school = School.objects.filter(
            Q(name__icontains=location_query) | 
            Q(name__icontains=normalized_query) |
            Q(kod_sekolah__iexact=location_query) |
            Q(city__icontains=location_query) |
            Q(postcode__icontains=location_query)
        ).first()

        if local_school and local_school.location:
            center_point = local_school.location
            search_source = "Database"
            lat = center_point.y
            lon = center_point.x

    # === LANGKAH 2: GEOCODING (External API - PHOTON) ===
    if not center_point:
        geo_data = geocode_location_smart(location_query)
        if geo_data:
            lat = geo_data['lat']
            lon = geo_data['lon']
            center_point = Point(lon, lat, srid=4326)
            search_source = "Photon API"
    
    # === LANGKAH 3: FALLBACK DATABASE ===
    if not center_point:
         extracted_postcode = re.search(r'\b\d{5}\b', location_query)
         proxy_school = None
         
         if extracted_postcode:
             proxy_school = School.objects.filter(postcode=extracted_postcode.group(0)).first()
         
         if not proxy_school:
             potential_city = location_query.split(',')[-1].strip()
             proxy_school = School.objects.filter(city__icontains=potential_city).first()

         if proxy_school and proxy_school.location:
            center_point = proxy_school.location
            search_source = "Database (Anggaran Kawasan)"
            lat = center_point.y
            lon = center_point.x

    if not center_point:
         return HttpResponse(f"<div class='alert alert-warning'>Lokasi '{location_query}' tidak ditemui. Cuba masukkan Poskod.</div>")

    # === LANGKAH 4: CARIAN RADIUS (SPATIAL) ===
    nearby_schools = School.objects.all()

    # --- LOGIK PENAPISAN JENIS SEKOLAH (DIRECT) ---
    if school_type and school_type != 'SEMUA':
        # Gunakan iexact untuk padanan tepat tetapi tidak sensitif huruf (case-insensitive)
        # Contoh: jika user pilih 'SK', ia akan cari 'SK' dalam database
        nearby_schools = nearby_schools.filter(school_type__iexact=school_type)

    # Lakukan pengiraan jarak spatial
    nearby_schools = nearby_schools.annotate(
        distance=Distance('location', center_point)
    ).filter(
        distance__lte=D(km=radius_km)
    ).order_by('distance')

    # Optimization
    schools_data = list(nearby_schools.values(
        'name', 'address', 'location', 'school_type', 'distance', 'photo', 'city', 'postcode'
    ))

    # Format JSON untuk Peta
    results_for_map = []
    for s in schools_data:
        dist_km = s['distance'].km 
        photo_url = None
        if s['photo']:
             photo_url = f"/media/{s['photo']}"

        results_for_map.append({
            'name': s['name'],
            'lat': s['location'].y,
            'lon': s['location'].x,
            'address': s['address'],
            'distance': round(dist_km, 2),
            'photo': photo_url
        })

    # Render HTML Sidebar
    context = {
        'schools': nearby_schools, 
        'search_query': location_query,
        'source': search_source
    }
    html = render_to_string('carian_sekolah/partials/results_list.html', context)
    
    # Respons HTMX
    response = HttpResponse(html)
    trigger_data = {
        'search_location': {'lat': lat, 'lon': lon},
        'schools': results_for_map
    }
    response['HX-Trigger'] = json.dumps({'updateMap': trigger_data})
    
    return response