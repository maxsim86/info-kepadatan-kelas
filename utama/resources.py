from import_export import resources
from .models import Classroom

class ClassroomResource(resources.ModelResource):
    class Meta:
        model = Classroom
        fields = ('school', 'year', 'average')
        