from django.shortcuts import render, redirect
from .forms import ClassroomForm
from .models import Classroom
from .resources import ClassroomResource
from django.http import HttpResponse
import pandas as pd
from .forms import ImportForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page


def check_availability(request):
    form = ClassroomForm(request.GET or None)

    if request.method == "POST":
        post_form = ClassroomForm(request.GET or None)

        if post_form.is_valid():
            post_form.save()
            return redirect("check_availability")

    selected_year = request.GET.get("year")
    selected_school = request.GET.get("school")
    classrooms = Classroom.objects.none()

    if selected_year and selected_school:
        classrooms = Classroom.objects.filter(
            year=selected_year, school=selected_school
        )

    context = {
        "form": form,
        "classrooms": classrooms,
        "selected_year": selected_year,
        "selected_school": selected_school,
    }
    if "HX-Request" in request.headers:
        html = render_to_string(
            "utama/partials/classroom_list.html", context, request=request
        )
        response = HttpResponse(html)
        response["HX-Trigger"] = "openModal"
        return response

    return render(request, "utama/check_availability.html", context)

@cache_page(60 * 15)
def school_data_json(request):
    """
    View ini menyediakan data sekolah dalam format JSON.
    Ia kini boleh menapis mengikut tahun jika parameter 'year' diberikan.
    """
    selected_year = request.GET.get("year", None)

    queryset = Classroom.objects.filter(latitude__isnull=False, longitude__isnull=False)

    if selected_year:
        schools_data = queryset.filter(year=selected_year).values(
            "id", "school", "latitude", "longitude", "average", "photo"
        )
    else:
        schools_data = queryset.values(
            "school", "latitude", "longitude", "photo"
        ).annotate(average=Max("average"), id=Max("id"))

    return JsonResponse(list(schools_data), safe=False)


@login_required
def export_data(request, file_format):
    classrooms = Classroom.objects.all()

    # Create a resource instance
    classroom_resource = ClassroomResource()

    # Export data to a DataFrame using pandas
    dataset = classroom_resource.export(queryset=classrooms)
    df = pd.DataFrame(dataset.dict)

    if file_format == "csv":
        response = HttpResponse(df.to_csv(index=False), content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="classrooms.csv"'
        return response
    elif file_format == "xls":
        response = HttpResponse(content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = 'attachment; filename="classrooms.xls"'
        df.to_excel(response, index=False)
        return response
    elif file_format == "json":
        response = HttpResponse(
            df.to_json(orient="records"), content_type="application/json"
        )
        response["Content-Disposition"] = 'attachment; filename="classrooms.json"'
        return response
    else:
        return HttpResponse("Invalid file format")


@login_required
def import_data(request):
    if request.method == "POST":
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]

            # Create a temporary file and write the content of the InMemoryUploadedFile to it
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(file.read())

            try:
                # Re-open the temporary file and read the Excel file
                df = pd.read_excel(temp_file.name, engine="openpyxl")

                # Perform further processing or save to the database
                Classroom.objects.bulk_create(
                    [Classroom(**row) for row in df.to_dict(orient="records")]
                )

                return redirect("success_page")

            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)

            finally:
                # Clean up: remove the temporary file
                temp_file.close()
                os.remove(temp_file.name)

    else:
        form = ImportForm()

    return render(request, "import.html", {"form": form})


# success url
def success_page(request):
    return render(request, "success_page.html")


def thank_you(request):
    return render(request, "thank_you.html")
