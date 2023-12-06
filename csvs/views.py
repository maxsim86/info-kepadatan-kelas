from django.shortcuts import render
from .forms import CsvModelForm
from .models import Csv
import csv
from utama.models import Info
# Create your views here.


def upload_file_view(request):
    form = CsvModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form = CsvModelForm()
        obj = Csv.objects.get(activated=False)
        with open(obj.file_name.path, "r") as f:
            reader = csv.reader(f)
            # Create a loop
            for i, row in enumerate(reader):
                if i == 0:
                    pass
                else:
                    row = "".join(row)
                    row = row.replace("", " ")
                    row = row.split()
                    
                    
                    
                    nama_sekolah = row[0].upper()
                    tahun = row[1].upper()
                    jumlah_kelas = int(row[2]).upper()
                    jumlah_murid = row[3].upper()
                    
                    Info.objects.create(
                        name = row[1],
                        tahun = row[2],
                        jumlah_kelas = row[3],
                        jumlah_murid = row[4],
                        
                        
                    )
                     #print(row)
                    #print(type(row))
            obj.activated = True
            obj.save()
    return render(request, "upload_csv.html", {"form": form})
