from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import FormView
from .models import Info
from .forms import InfoFilterForm, InfoSelectForm
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