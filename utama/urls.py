# urls.py
from django.urls import path
from . import views

app_name = 'utama'

urlpatterns = [
    path('pengecekan_kelas/',views.check_availability, name='check_availability'),
    path('/export_csv/', views.export_csv, name='export_csv'),
]
