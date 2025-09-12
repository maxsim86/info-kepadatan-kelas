from django.urls import path
from .import views

app_name = 'carian_sekolah'

urlpatterns = [
        path('', views.paparan_pencari, name='paparan_pencari'),
        path('api/search/', views.search_and_find_schools, name='api_search_and_find'),
        path('api/autocomplete-address/', views.address_autocomplete, name='address_autocomplete'),
        path('school/<int:school_id>/submit-image/', views.submit_school_image, name='submit_school_image'),
        path('submission-thank-you/', views.submission_thank_you, name='submission_thank_you'),
]
