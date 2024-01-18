from django.contrib import admin
from . models import Classroom



admin.site.register(Classroom)

# meta override.
#  class meta dalam admin.
#ambik direct

#clean method
#simpan data 
#save data untuk user submit
#many to many table
# class dan ada murid,one to many
#simpan reference pada sekolah dan kelas 