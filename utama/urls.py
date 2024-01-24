# urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('',views.check_availability, name='check_availability'),
    path('export_csv/', views.export_csv, name='export_csv'),
    path('import_csv/', views.import_csv, name='import_csv'),
    path('/', views.contact_us, name='contact_us'),
    
]
