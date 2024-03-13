from django.urls import path
from . import views


urlpatterns = [
    path("", views.indexKuiz, name='index_kuiz'),
    path("quiz/<int:quiz_id>", views.quizDetail, name='quiz_detail'),

]
