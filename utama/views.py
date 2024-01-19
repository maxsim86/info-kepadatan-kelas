from django.shortcuts import render, redirect
from .forms import ClassroomForm
from .models import Classroom
from django.template.loader import render_to_string
from django.http import HttpResponse


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
    
    context = {'form':form, 'classrooms':classrooms, 'selected_year':year, 'class_name_filter':class_name_filter, 'school':school_name, 'query':''}
    # Jika request menggunakan htmx, kembalikan hanya content nya sahaja
    
    if request.headers.get('HTTP_HX_REQUEST') == 'true':
        html_content = render_to_string('classroom_list.html', context)
        return HttpResponse(html_content)
     
    return render(request, 'check_availability.html', context)

    