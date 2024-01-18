# urls.py
from django.urls import path
from . import views
from .views import search_school

app_name = 'utama'

urlpatterns = [
    path('search/', search_school, name='search_school'),
    path('pengecekan_kelas/',views.check_availability, name='check_availability'),
]
