from django.shortcuts import render, redirect
from .forms import ClassroomForm, ContactForm
from .models import Classroom
from django.urls import reverse
from .resources import ClassroomResource
from django.http import HttpResponse
import pandas as pd
from .forms import ImportForm
from django.http import JsonResponse
import chardet, tempfile, os, openpyxl

                     

def check_availability(request):
    form = ClassroomForm()

    if request.method=='POST':
        form = ClassroomForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('check_availability')

    classrooms = Classroom.objects.all()

    # Filter berdasarkan sekolah dan tahun
    year = request.GET.get('year', 'PPKI')
    school_name = request.GET.get('school', 'SMK TAMAN KLANG UTAMA')
    class_name_filter = request.GET.get('class_name', '')
    classrooms = Classroom.objects.filter(year=year, school__icontains=school_name)

    
    context = {'form':form, 'classrooms':classrooms, 'selected_year':year, 'class_name_filter':class_name_filter, 'school':school_name}
    return render(request, 'check_availability.html', context)
    
def export_data(request, file_format):
    classrooms = Classroom.objects.all()

    # Create a resource instance
    classroom_resource = ClassroomResource()

    # Export data to a DataFrame using pandas
    dataset = classroom_resource.export(queryset=classrooms)
    df = pd.DataFrame(dataset.dict)

    if file_format == 'csv':
        response = HttpResponse(df.to_csv(index=False), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="classrooms.csv"'
        return response
    elif file_format == 'xls':
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="classrooms.xls"'
        df.to_excel(response, index=False)
        return response
    elif file_format == 'json':
        response = HttpResponse(df.to_json(orient='records'), content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="classrooms.json"'
        return response
    else:
        return HttpResponse("Invalid file format")
    

def import_data(request):
    if request.method == 'POST':
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']

            # Create a temporary file and write the content of the InMemoryUploadedFile to it
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(file.read())

            try:
                # Re-open the temporary file and read the Excel file
                df = pd.read_excel(temp_file.name, engine='openpyxl')

                # Perform further processing or save to the database
                Classroom.objects.bulk_create([
                    Classroom(**row) for row in df.to_dict(orient='records')
                ])

                return redirect('success_page')

            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)

            finally:
                # Clean up: remove the temporary file
                temp_file.close()
                os.remove(temp_file.name)

    else:
        form = ImportForm()

    return render(request, 'import.html', {'form': form})

#success url
def success_page(request):
    return render(request, 'success_page.html')
            


def contact_us(request):
    # POST REQUEST --> FORM CONTENTS --> THANK YOU
    if request.method == 'POST': 
        form = ContactForm(request.POST)
        
        if form.is_valid():
            # simpan di DB admin
            form.save()
            return redirect(reverse('thank_you'))
    # ELSE, RENDER FORM
    else:
        form = ContactForm()
    return render(request, 'contact_us.html', context={'form':form})

def thank_you(request):
    return render(request, 'thank_you.html')