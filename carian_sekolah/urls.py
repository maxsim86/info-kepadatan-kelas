from django.urls import path
from .import views

app_name = 'carian_sekolah'

urlpatterns = [
        path('', views.paparan_pencari, name='paparan_pencari'),
        #path('api/nearby-schools/', views.find_nearby_schools, name='api_find_nearby_schools'),
        path('api/search/', views.search_and_find_schools, name='api_search_and_find'),
]
