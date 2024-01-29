from django.shortcuts import render, redirect
from .forms import ClassroomForm, ContactForm
from .models import Classroom
from django.urls import reverse

import pandas as pd
from django.http import HttpResponse


def process_csv_pandas(csv_file):
    # Read CSV file using Pandas
    df = pd.read_csv(csv_file, delimiter='\t')

    # Iterate through rows and create or update Classroom objects
    for index, row in df.iterrows():
        school = row.get('school', '')
        year = row.get('year', '')
        average = row.get('average', '')

        if school and year and average:
            try:
                # Try to get an existing Classroom object
                classroom_object = Classroom.objects.get(school=school, year=year)
                # If it exists, update its values
                classroom_object.average = average
                classroom_object.save()
            except Classroom.DoesNotExist:
                # If it doesn't exist, create a new Classroom object
                Classroom.objects.create(school=school, year=year, average=average)
                     

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

    
    context = {'form':form, 'classrooms':classrooms, 'selected_year':year, 'class_name_filter':class_name_filter, 'school':school_name,}
    return render(request, 'check_availability.html', context)
    
def export_csv(request):
    # Fetch data from the database
    classrooms = Classroom.objects.all()

    # Create a DataFrame using Pandas
    df = pd.DataFrame(list(classrooms.values('school', 'year', 'average')))

    # Create a response with CSV content
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="classroom.csv"'

    # Write DataFrame to CSV
    df.to_csv(path_or_buf=response, index=False, sep='\t')

    return response
    

            
def import_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        process_csv_pandas(csv_file)
        return redirect('check_availability')

    return render(request, 'import_csv.html')


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