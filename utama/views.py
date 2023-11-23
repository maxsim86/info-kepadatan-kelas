from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import StudentColorForm
from django.views import View
from django.http import JsonResponse
from django.urls import reverse_lazy
# Create your views here.
class StudentColorView(FormView):
    template_name = 'student_color.html'
    form_class = StudentColorForm
    
    def form_valid(self, form):
        is_ajax = self.request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

        sekolah = form.cleaned_data['sekolah']
        tahun = form.cleaned_data['tahun']
        jum_kelas = form.cleaned_data['jum_kelas']
        jum_murid = form.cleaned_data['jum_murid']
        purata_str = form.cleaned_data['purata']
         
        purata = self.calculate_purata(purata_str, jum_kelas, jum_murid )


        color, message, _ = self.calculate_color_and_message(purata, jum_kelas,jum_murid)

        data = {
                'color': color,
                'message': message,
                'sekolah': sekolah,
                'tahun': tahun,
                'jum_kelas': jum_kelas,
                'jum_murid': jum_murid,
                'purata': purata,
            }

        if is_ajax:
            return JsonResponse(data)
        return super().form_valid(form)
    
    def calculate_purata(self, purata_str, jum_kelas, jum_murid):
        if purata_str:
            try:
                return int(purata_str)
            except ValueError:
                return 0
        else:
            return jum_murid / jum_kelas if jum_kelas > 0 else 0
    
    
    def calculate_color_and_message(self, purata, jum_kelas, jum_murid):
        if purata >= 40:
            color = 'red'
            message = f"Purata ({purata}) melebihi 40. Lihat Kelas Detail"

        elif jum_kelas /jum_murid <= 40:
            color = 'green'
            message = f"Purata ({purata}). Penuh. Lihat Kelas Detail "
        else:
            color = 'blue'
            message = "Lihat Kelas Detail"
        
        return color, message, purata
                

    def get_success_url(self):
        purata_str = self.request.POST.get('purata', 0)
        try:
            purata = int(purata_str)
        except ValueError:
            purata = 0

        if purata >= 40:
            return reverse_lazy('high_purata')
        else:
            return reverse_lazy('low_purata')
        

class HighPurataView(View):
    template_name = 'high_purata.html'
    
    def get(self, request, *args, **kwargs):
        
        color='red'
        
        context = {
            'color':color,
        }
        return render(request, self.template_name, context)
    
class LowPurataView(View):
    template_name = 'low_purata.html'
    def get(self, request, *args, **kwargs):

        color='green'
        context ={
            'color':color,
            'message': 'Here is your output value'
        
        }
        
        return render(request, self.template_name, context)

    
class CalculateAverageView(View):
    def get(self, request, *args, **kwargs):
        # Handle GET request to retrieve the initial value or for debugging
        average = float(request.GET.get('average', 0.0))
        return JsonResponse({'average': average})
    
    def post(self, request, *args, **kwargs):
        jum_murid = float(request.POST.get('jum_murid', 0))
        purata = float(request.POST.get('purata', 0))
        
        if jum_murid > 0:
            average = purata / jum_murid
        else:
            average = 0.0
        return JsonResponse({'average':average})
