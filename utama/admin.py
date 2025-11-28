from django.contrib import admin
from .models import Classroom
from import_export.admin import ImportExportModelAdmin


@admin.register(Classroom)
class EmployeeAdmin(ImportExportModelAdmin):
    pass
