# urls.py
from django.urls import path
from .views import StudentColorView, CalculateAverageView, CSVUploadView
#HighPurataView, LowPurataView

urlpatterns = [
    #path('items/select_info/', InfoSelectView.as_view(), name='select_view'),
    path('', StudentColorView.as_view(), name='student_color'),
    path('calculate_average/', CalculateAverageView.as_view(), name='calculate_average'),
    path('upload-csv/', CSVUploadView.as_view(), name='upload_csv' ),
#    path('high-purata/', HighPurataView.as_view(), name='high_purata'),
    #path('low-purata/', LowPurataView.as_view(), name='low_purata'),
]

