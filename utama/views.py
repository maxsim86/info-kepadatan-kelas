from django.shortcuts import render
from django.views.generic import ListView, FormView
from .models import Info
from .forms import InfoFilterForm
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
