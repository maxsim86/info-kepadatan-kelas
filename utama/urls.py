# urls.py
from django.urls import path
from .views import StudentColorView, CalculateAverageView, ImportCSVView, ExportCSVView

# HighPurataView, LowPurataView
from . import views



urlpatterns = [
    path("check_kelas/", views.check_availlability, name="check_availability"),
    # path('items/select_info/', InfoSelectView.as_view(), name='select_view'),
    path("", StudentColorView.as_view(), name="student_color"),
    path(
        "calculate_average/", CalculateAverageView.as_view(), name="calculate_average"
    ),
    path("import-csv/", ImportCSVView.as_view(), name="import_csv"),
    path("export-csv/", ExportCSVView.as_view(), name="export_csv"),
    # path('high-purata/', HighPurataView.as_view(), name='high_purata'),
    # path('low-purata/', LowPurataView.as_view(), name='low_purata'),
]
