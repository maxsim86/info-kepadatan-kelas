from django.contrib import admin
from .models import ListSekolah
from .forms import StudentColorForm
from .models import Info, TahunModel

admin.site.unregister(Info)

# Register your models here.


class StudentColorAdmin(admin.ModelAdmin):
    form = StudentColorForm
    list_display = ("name", "list_sek", "no_ic", "jum_kelas", "jum_murid")

    def save_model(self, request, obj, form, change):
        obj.jum_murid = form.cleaned_data["jum_murid"]
        obj.save()


admin.site.register(Info, StudentColorAdmin)
admin.site.register(ListSekolah)
admin.site.register(TahunModel)



# meta override.
#  class meta dalam admin.
#ambik direct

#clean method
#simpan data 
#save data untuk user submit
#many to many table
# class dan ada murid,one to many
#simpan reference pada sekolah dan kelas 