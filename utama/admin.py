from django.contrib import admin
from . models import Classroom, Contact_us
from import_export.admin import ImportExportModelAdmin

admin.site.register(Contact_us)

@admin.register(Classroom)

class EmployeeAdmin(ImportExportModelAdmin):
    pass
