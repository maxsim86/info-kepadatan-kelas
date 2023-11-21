# urls.py
from django.urls import path
from .views import InfoSelectView, SuccessView, StudentColorView, CalculateAverageView, HighPurataView, LowPurataView

urlpatterns = [
    path('items/select_info/', InfoSelectView.as_view(), name='select_view'),
    path('', StudentColorView.as_view(), name='student_color'),
    path('success/', SuccessView.as_view(), name='success'),
    path('calculate_average/', CalculateAverageView.as_view(), name='calculate_average'),
    path('high-purata/', HighPurataView.as_view(), name='high_purata_url'),
    path('low-purata/', LowPurataView.as_view(), name='low_purata_url'),
]
]
