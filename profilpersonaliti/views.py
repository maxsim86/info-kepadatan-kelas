from django.shortcuts import render, get_object_or_404
from .models import *
# Create your views here.
def indexKuiz(request):
    quizzes = Quiz.objects.filter(is_ready_to_publish = True)
    context = {"quizzes":quizzes}
    return render(request, 'index_kuiz.html', context=context)

def quizDetail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    context = {"quiz":quiz, "questions":questions}
    return render(request, 'quiz_detail.html',  context)