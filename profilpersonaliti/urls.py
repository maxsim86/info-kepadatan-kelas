from django.urls import path
from . import views


urlpatterns = [
    path("", views.indexQuiz, name='index_quiz'),
    path("quiz/<int:quiz_id>", views.quizDetail, name='quiz_detail'),
    path("quiz/<int:quiz_id>/submit", views.quiz_submit,  name='quiz_submit'),

]
