from django.shortcuts import render
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.http import JsonResponse
from .models import School

# Create your views here.
def paparan_pencari(request):
    """
    View ini akan memaparkan halaman utama untuk aplikasi pencari sekolah,
    yang mengandungi peta dan borang carian.
    """
    # Buat masa ini, kita tidak perlukan sebarang konteks data
    context = {}
    return render(request, 'carian_sekolah/pencari.html', context)

    
def find_nearby_schools(request):
    """
    API endpoint untuk mencari sekolah dalam radius tertentu
    dari satu titik koordinat.
    """
    try:
        lat = float(request.GET.get('lat'))
        lon = float(request.GET.get('lon'))
        radius_km = float(request.GET.get('radius'))
    except (TypeError, ValueError):
        # Kembalikan ralat jika parameter tidak sah atau tiada
        return JsonResponse({'error': 'Parameter lat, lon, dan radius tidak sah.'}, status=400)

    user_location = Point(lon, lat, srid=4326)

    # Cari sekolah yang lokasinya berada dalam radius dari lokasi pengguna
    # dan susun mengikut jarak terdekat
    nearby_schools = School.objects.filter(
        location__distance_lte=(user_location, D(km=radius_km))
    ).values('name', 'address', 'location')

    # Tukar PointField kepada lat/lon biasa untuk JSON
    results = []
    for school in nearby_schools:
        results.append({
            'name': school['name'],
            'address': school['address'],
            'lat': school['location'].y, # .y adalah latitud
            'lon': school['location'].x, # .x adalah longitud
        })

    return JsonResponse(results, safe=False)