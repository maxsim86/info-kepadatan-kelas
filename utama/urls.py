# urls.py
from django.urls import path
from . import views


urlpatterns = [
    path("", views.check_availability, name="check_availability"),
    # import dan export data
    path("export/<str:file_format>/", views.export_data, name="export_data"),
    path("import/", views.import_data, name="import_data"),
    path("api/data-sekolah/", views.school_data_json, name="school_data_json"),
    path("thank_you/", views.thank_you, name="thank_you"),
    path("success/", views.success_page, name="success_page"),
]
