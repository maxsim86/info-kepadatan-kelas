# urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('',views.check_availability, name='check_availability'),
    path('export/<str:file_format>/', views.export_data, name='export_data'),
    path('import/', views.import_data, name='import_data'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('thank_you/', views.thank_you, name='thank_you'),
    path('success/', views.success_page, name='success_page' ),
    
]
