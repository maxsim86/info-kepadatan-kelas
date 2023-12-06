# urls.py
from django.urls import path
from .views import StudentColorView, CalculateAverageView, ImportCSVView, ExportCSVView
#HighPurataView, LowPurataView
from csvs.views import upload_file_view


urlpatterns = [
    #path('items/select_info/', InfoSelectView.as_view(), name='select_view'),
    path('', StudentColorView.as_view(), name='student_color'),
    path('calculate_average/', CalculateAverageView.as_view(), name='calculate_average'),
    path('import-csv/', ImportCSVView.as_view(), name='import_csv' ),
    path('export-csv/', ExportCSVView.as_view(), name='export_csv' ),
    path('upload-csv/', upload_file_view, name='upload-view'),
    #path('high-purata/', HighPurataView.as_view(), name='high_purata'),
    #path('low-purata/', LowPurataView.as_view(), name='low_purata'),

]

