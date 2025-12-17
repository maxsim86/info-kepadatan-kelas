import requests
import json
import re
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import School
from .forms import ImageSubmissionForm
from django.contrib.gis.db.models.functions import Distance
from django.core.cache import cache
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

#untuk muat naik gambar
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

#Page submission thank you
def submission_thank_you(request):
    return render(request, "carian_sekolah/submission_thank_you.html")


# enjin carian
def paparan_pencari(request):
    ppd_list = School.objects.order_by("ppd").values_list("ppd", flat=True).distinct()
    context = {"ppd_list": ppd_list}
    return render(request, "carian_sekolah/pencari.html", context)


def geocode_location(location_query):
    cache_key = f"geodata_{location_query.lower().replace(' ', '_')}"
    cached_location = cache.get(cache_key)
    if cached_location:
        return cached_location, location_query

    search_queries = [location_query]
    postcode_match = re.search(r"\b\d{5}\b", location_query)
    if postcode_match:
        search_queries.append(postcode_match.group(0))

    for query in search_queries:
        nominatim_url = f"https://nominatim.openstreetmap.org/search?format=json&q={query}, Malaysia"
        try:
            response = requests.get(
                nominatim_url, headers={"User-Agent": "SchoolLocatorApp/1.0"}
            )
            response.raise_for_status()
            geodata = response.json()
            if geodata:
                lat = float(geodata[0]["lat"])
                lon = float(geodata[0]["lon"])
                search_location = {"lat": lat, "lon": lon}
                cache.set(cache_key, search_location, 86400)
                return search_location, query
        except (requests.RequestException, IndexError, KeyError):
            continue

    return None, location_query


def address_autocomplete(request):
    query = request.GET.get("location", "").strip()
    suggestions = []
    if len(query) > 3:  # Hanya cari jika input lebih dari 3 aksara
        nominatim_url = f"https://nominatim.openstreetmap.org/search?format=json&q={query}, Malaysia&limit=5"
        try:
            # Gunakan library untuk 'requests' yang telah diimport
            response = requests.get(
                nominatim_url, headers={"User-Agent": "SchoolLocatorApp/1.0"}
            )
            response.raise_for_status()
            geodata = response.json()
            suggestions = [result["display_name"] for result in geodata]

        except (requests.RequestException, IndexError, KeyError):
            pass

    return render(
        request,
        "carian_sekolah/partials/autocomplete_results.html",
        {"suggestions": suggestions},
    )

def search_and_find_schools(request):
    location_query = request.GET.get("location", "").strip()
    school_type = request.GET.get("type", "SEMUA").upper()
    radius_km = float(request.GET.get("radius", 3.0))
    ppd_query = request.GET.get("ppd", "").strip()
    page_number = request.GET.get("page", 1)
    is_initial_search = request.GET.get("initial") == "true"

    if not location_query and not ppd_query:
        return HttpResponse("")

    direct_matches_query = School.objects.none()
    geocoded_matches_query = School.objects.none()
    ppd_matches_query = School.objects.none()

    search_location = None
    successful_query = None

    # 2. Lakukan carian teks jika ada input lokasi
    if location_query:
        vector = SearchVector("name", "address", "postcode")
        search_query = SearchQuery(location_query)
        direct_matches_query = School.objects.annotate(
            rank=SearchRank(vector, search_query)
        ).filter(rank__gte=0.01)

        # carian menggunakan by geografi
        search_location, successful_query = geocode_location(location_query)
        if search_location:
            user_location_point = Point(
                search_location["lon"], search_location["lat"], srid=4326
            )
            geocoded_matches_query = School.objects.filter(
                location__distance_lte=(user_location_point, D(km=radius_km))
            )

    # 3. Lakukan carian PPD jika dipilih
    if ppd_query:
        ppd_matches_query = School.objects.filter(ppd__iexact=ppd_query)

    #if ppd_query:
    #    ppd_matches_query = School.objects.filter(ppd__iexact=ppd_query)

    # Jika ada carian lokasi, gabungkan hasil teks dan geografi
    if location_query:
        combined_query = (direct_matches_query | geocoded_matches_query).distinct()
        # Jika PPD juga dipilih, tapis lagi hasil gabungan itu
        if ppd_query:
            combined_query = combined_query.filter(ppd__iexact=ppd_query)
    else:
        # Jika tiada carian lokasi, hasil carian hanyalah dari PPD
        combined_query = ppd_matches_query

    # Tapis jenis sekolah pada hasil akhir
    if school_type in ["RENDAH", "MENENGAH"]:
        combined_query = combined_query.filter(school_type=school_type)

    if search_location:
        user_location_point = Point(
            search_location["lon"], search_location["lat"], srid=4326
        )
        final_query = (
            combined_query.annotate(distance=Distance("location", user_location_point))
            .filter(distance__lte=D(km=radius_km))
            .order_by("distance")
        )
    else:
        final_query = combined_query.order_by("name")

    # 6. Paginasi, papar page 10 per page
    paginator = Paginator(final_query, 10)
    page_obj = paginator.get_page(page_number)

    # 7. Sediakan data untuk frontend
    results_for_js = []
    if is_initial_search:
        for school_obj in final_query:
            photo_url = school_obj.photo.url if school_obj.photo else None
            results_for_js.append(
                {
                    "id": school_obj.id,
                    "name": school_obj.name,
                    "lat": school_obj.location.y,
                    "lon": school_obj.location.x,
                    "photo_url": photo_url,
                    "school_type": school_obj.school_type,
                }
            )

    context = {
        "page_obj": page_obj,
        "search_location_found": bool(search_location),
        "geocoding_failed": not bool(search_location) and bool(location_query),
        "location_query": location_query,
        "successful_query": (
            successful_query
            if not bool(search_location) and successful_query != location_query
            else None
        ),
        "request": request,
    }
    html = render_to_string("carian_sekolah/partials/results_list.html", context)

    response = HttpResponse(html)
    if is_initial_search:
        trigger_data = {"search_location": search_location, "schools": results_for_js}
        response["HX-Trigger"] = json.dumps({"updateMap": trigger_data})

    return response

