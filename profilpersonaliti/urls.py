from django.urls import path
from . import views


urlpatterns = [
    path("", views.indexQuiz, name="index_quiz"),
    path("quiz/<int:quiz_id>", views.quizDetail, name="quiz_detail"),
    path("quiz/<int:quiz_id>/submit", views.quiz_submit, name="quiz_submit"),
    path("score_percentage", views.jadual_score_percentage, name="score_percentage"),
    path('signup/', views.SignUpView.as_view(), name='signup')
    #    path(
    #       "quiz/<int:quiz_id>/score_percentage",
    #       views.score_percentage,
    #       name="score_percentage",
    #   ),
]
