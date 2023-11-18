from django.contrib import admin
from .models import Info, ListSekolah
from .forms import StudentColorForm

# Register your models here.


class StudentColorAdmin(admin.ModelAdmin):
    form = StudentColorForm
    list_display = ('jum_kelas', 'jum_murid')

admin.site.register(Info, StudentColorAdmin)
admin.site.register(ListSekolah)