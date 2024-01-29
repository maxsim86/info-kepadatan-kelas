from django.shortcuts import render, redirect
from .forms import ClassroomForm, ContactForm
from .models import Classroom
from django.urls import reverse

import csv
from django.http import HttpResponse

def process_csv(csv_file):
    decoded_file = csv_file.read().decode('utf-8').splitlines()
    reader = csv.DictReader(decoded_file, delimiter='\t')
    
    for row in reader:
        print(f"School: {row.get('school', '')}, Year: {row.get('year', '')}, Average: {row.get('average', '')}")
        school = row.get('school', '')
        year = row.get('year', '')
        average = row.get('average', '')
        
        if school and year and average:
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
    
    context = {'form':form, 'classrooms':classrooms, 'selected_year':year, 'class_name_filter':class_name_filter, 'school':school_name}
    return render(request, 'check_availability.html', context)
    

def export_csv(request):
    # Ambil data dari database
    classrooms = Classroom.objects.all()

    # Membuat object HttpResponse dengan content CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition']= 'attachment'; filename="classroom.csv"
    #Membuat object writer CSV dan menulis header
    writer = csv.writer(response)
    writer.writerow(['Nama Sekolah', 'Tahun', 'Purata'])

    # Menulis setiap baris data ke file CSV
    for classroom in classrooms:
        writer.writerow([classroom.school, classroom.year, classroom.average ])
    return response
    

            
def import_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        process_csv(csv_file)
        return redirect('check_availability')

    return render(request, 'import_csv.html')


def contact_us(request):
    # POST REQUEST --> FORM CONTENTS --> THANK YOU
    if request.method == 'POST': 
        form = ContactForm(request.POST)
        
        if form.is_valid():
            print(form.cleaned_data)
            return redirect(reverse('thank_you'))
    # ELSE, RENDER FORM
    else:
        form = ContactForm()
    return render(request, 'contact_us.html', context={'form':form})

def thank_you(request):
    return render(request, 'thank_you.html')