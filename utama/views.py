from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import StudentColorForm, SCVUploadForm
from django.views import View
from django.http import JsonResponse
from django.urls import reverse_lazy

# import csv module
import csv
from .models import Info, TahunModel, ListSekolah
from django.http import HttpResponse


# Create your views here.
class StudentColorView(FormView):
    template_name = "student_color.html"
    form_class = StudentColorForm

    def form_valid(self, form):
        tahun = form.cleaned_data["tahun"]
        jum_kelas = form.cleaned_data["jum_kelas"]
        jum_murid = form.cleaned_data["jum_murid"]
        purata_str = form.cleaned_data["purata"]
        purata = self.calculate_purata(purata_str, jum_kelas, jum_murid)

        color, message, purata = self.calculate_color_and_message(
            purata, jum_kelas, jum_murid
        )
        # simpan form kedalam db
        form.save()

        data = {
            "color": color,
            "message": message,
            "tahun": tahun,
            "jum_kelas": jum_kelas,
            "jum_murid": jum_murid,
            "purata": purata,
        }
        if purata >= 40:
            # success_url = reverse_lazy('high_purata')
            return render(self.request, "high_purata.html", data)
        else:
            # success_url =reverse_lazy('low_purata')
            return render(self.request, "low_purata.html", data)

    def calculate_purata(self, purata_str, jum_kelas, jum_murid):
        if purata_str:
            try:
                return int(purata_str)
            except ValueError:
                return 0
        else:
            jum_kelas = int(jum_kelas) if jum_kelas else 0
            jum_murid = int(jum_murid) if jum_murid else 0

            if jum_kelas > 0:
                return jum_murid / jum_kelas

            else:
                return 0

    def calculate_color_and_message(self, purata, jum_kelas, jum_murid):
        if purata >= 40:
            color = "red"
            message = f"Purata ({purata}) melebihi 40. Lihat Kelas Detail"

        elif jum_murid and jum_kelas and jum_kelas / jum_murid <= 40:
            color = "green"
            message = f"Purata ({purata}). Penuh. Lihat Kelas Detail "
        else:
            color = "blue"
            message = "Lihat Kelas Detail"

        return color, message, purata

    def get_success_url(self):
        purata_str = self.request.POST.get("purata", 0)
        try:
            purata = int(purata_str)
        except ValueError:
            purata = 0

        if purata >= 40:
            return reverse_lazy("high_purata")
        else:
            return reverse_lazy("low_purata")


class CalculateAverageView(View):
    def get(self, request, *args, **kwargs):
        # Handle GET request to retrieve the initial value or for debugging
        average = float(request.GET.get("average", 0.0))
        return JsonResponse({"average": average})

    def post(self, request, *args, **kwargs):
        jum_murid = float(request.POST.get("jum_murid", 0))
        purata = float(request.POST.get("purata", 0))

        if jum_murid > 0:
            average = purata / jum_murid
        else:
            average = 0.0
        return JsonResponse({"average": average})


class ImportCSVView(View):
    template_name = "upload_csv.html"

    def get(self, request, *args, **kwargs):
        form = SCVUploadForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = SCVUploadForm(request.POST, request.FILES)

        if form.is_valid():
            csv_file = request.FILES["csv_file"]
            decode_file = csv_file.read().decode("utf-8").splitlines()
            reader = csv.DictReader(decode_file)

            for row in reader:
                tahun_instance, created = TahunModel.objects.get_or_create(
                    tahun=row.get("tahun", "")
                )
                list_sekolah_instance, created = ListSekolah.objects.get_or_create(
                    kod_sekolah=row.get("list_kod_sekolah", "")
                )

                jum_kelas = int(row["jum_kelas"] if row.get("jum_kelas") else 0)
                jum_murid = int(row["jum_murid"]) if row.get("jum_murid") else 0

                try:
                    jum_kelas = int(row["jum_kelas"]) if row.get("jum_kelas") else 0
                except ValueError:
                    jum_kelas = 0

                try:
                    jum_murid = int(row["jum_murid"]) if row.get("jum_murid") else 0
                except ValueError:
                    jum_murid = 0

                Info.objects.create(
                    list_kod_sekolah=list_sekolah_instance,
                    tahun=tahun_instance,
                    jum_kelas=row.get("jum_kelas", 0),
                    jum_murid=row.get("jum_murid", 0),
                )

        return render(request, self.template_name, {"form": form})


class ExportCSVView(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type="text/csv")
        response["content-Disposition"] = 'attachment; filename="exported_data.svc"'

        writer = csv.writer(response)
        writer.writerow(
            [
                "Name",
                "No Tel",
                "No IC",
                "Email",
                "Tahun",
                "Jum kelas",
                "jumlah Murid",
                "Purata",
                "List Sekolah",
                "kod Sekolah",
            ]
        )

        infos = Info.objects.all()
        for info in infos:
            writer.writerow(
                [
                    info.name,
                    info.no_tel,
                    info.no_ic,
                    info.email,
                    info.list_kod_sekolah,
                    info.tahun,
                    info.jum_kelas,
                    info.jum_murid,
                    info.purata,
                ]
            )

        return response
