# urls.py
from django.urls import path
from .views import InfoListView, InfoFilterView, InfoSelectView, SuccessView, StudentColorView, CalculateAverageView

urlpatterns = [
    path('items/', InfoListView.as_view(), name='item_list'),
    path('items/filter/', InfoFilterView.as_view(), name='item_filter'),
    path('items/select_info/', InfoSelectView.as_view(), name='select_view'),
    path('items/student_color/', StudentColorView.as_view(), name='student_color'),
    path('success/', SuccessView.as_view(), name='success'),
    path('calculate_average/', CalculateAverageView.as_view(), name='calculate_average'),
    # tambahkan url lain sesuai kebutuhan
]
