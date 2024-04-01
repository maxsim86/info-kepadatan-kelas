from import_export import resources
from .models import Classroom
from profilpersonaliti.models import Question


class ClassroomResource(resources.ModelResource):
    class Meta:
        model = Classroom
        fields = ("school", "year", "average")
        exclude = ("id",)


class QuestionResource(resources.ModelResource):
    class Meta:
        model = Question
        fields = ("text", "quiz")
        exclude = ("id",)
