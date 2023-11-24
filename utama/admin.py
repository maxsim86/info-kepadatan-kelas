from django.contrib import admin
from .models import ListSekolah
from .forms import StudentColorForm 
from .models import Info, TahunModel
#Unregister the existhing registration of Info
admin.site.unregister(Info)

# Register your models here.

#class InfoAdmin(admin.ModelAdmin):
#    form = AdminStudentColorForm
    
class StudentColorAdmin(admin.ModelAdmin):
    form = StudentColorForm
    list_display = ('name','list_sek', 'no_ic', 'jum_kelas', 'jum_murid')

admin.site.register(Info, StudentColorAdmin)
admin.site.register(ListSekolah)
admin.site.register(TahunModel)