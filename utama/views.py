from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import FormView
from .models import Info
from .forms import InfoFilterForm, InfoSelectForm, StudentColorForm
from django.views import View
# Create your views here.


class InfoListView(ListView):
    model = Info
    template_name = 'item_list.html'
    context_object_name = 'infos'

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        # tambahkan logika filter lain sesuai kebutuhan
        return queryset

class InfoFilterView(FormView):
    form_class = InfoFilterForm
    template_name = 'item_list.html'

    def form_valid(self, form):
        # Redirect ke halaman item_list dengan parameter query yang sesuai
        return self.redirect('item_list', **form.cleaned_data)

# Pilihan Pilih Senarai Sekolah
class InfoSelectView(FormView):
    template_name="select_item.html"
    form_class=InfoSelectForm
    success_url="/success" # tentukan url mengikut keperluan
    
    def form_valid(self, form):
        #Lakukan sesuatu item yang dipilih 
        selected_item = form.cleaned_data['listsekolah']
        return super().form_valid(form)
    
class StudentColorView(FormView):
    template_name = 'student_color.html'
    form_class = StudentColorForm
    success_url = None
    
    def form_valid(self, form):
        sekolah = form.cleaned_data['sekolah']
        tahun = form.cleaned_data['tahun']
        # untuk dapatkan Purata = jum_kelas / jumlah murid
        jum_kelas = form.cleaned_data['jum_kelas']
        jum_murid = form.cleaned_data['jum_murid']
        purata = form.cleaned_data['purata']

        if jum_murid >= 40:
            color = 'yellow'
            message = f"The average ({purata}) does not exceed 40. Full class details:"
                        

        elif purata > 40:
            color = 'red'
            message = f"The average ({purata}) exceeds 40. Class details:"
            

        else:
            color = 'green'
            message = "Class Detail"
        # Add color data to the context    
        self.extra_context = {
            'color':color,
            'message': message,
            'sekolah':sekolah,
            'tahun':tahun,
            'jum_kelas': jum_kelas,
            'jum_murid': jum_murid,
            'purata': purata,
                              }
        return self.render_to_response(self.get_context_data(form=form))
       # return super().form_valid(form)
    
class SuccessView(View):
    template_name = 'success.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)