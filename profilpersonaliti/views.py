from django.shortcuts import render, get_object_or_404, redirect
from profilpersonaliti.models import Quiz, Question, Choice, UserResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count


# Create your views here.
def indexQuiz(request):
    quizzes = Quiz.objects.filter(is_ready_to_publish=True)
    context = {"quizzes": quizzes}
    return render(request, "index_quiz.html", context=context)


# detail quiz
@login_required(login_url="login")
def quizDetail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    context = {"quiz": quiz, "questions": questions}
    return render(request, "quiz_detail.html", context)


# submit quiz and calculate total score  base on AS, AN, KD, KP, JD, PT, SB,
# PN,PN, IG, PM, KC, KS


def count_choices(request, quiz_id):
    # count(ASERTIF)
    count_as = (
        Question.objects.filter(quiz_id=quiz_id)
        .values("AS", "quiz_id")
        .annotate(total=Count("AS"))
    )

    # count AN(ANALITIKAL)
    count_an = (
        Question.objects.filter(quiz_id=quiz_id)
        .values("AN", "quiz_id")
        .annotate(total=Count("AN"))
    )
    # count KP(KEYAKINAN DIRI)
    count_kp = (
        Question.objects.filter(quiz_id=quiz_id)
        .values("KP", "quiz_id")
        .annotate(total=Count("KP"))
    )
    # cout JD(JATI DIRI)
    count_jd = (
        Question.objects.filter(quiz_id=quiz_id)
        .values("JD", "quiz_id")
        .annotate(total=Count("JD"))
    )
    # count PT(PRIHATIN)
    count_pt = (
        Question.objects.filter(quiz_id=quiz_id)
        .values("PT", "quiz_id")
        .annotate(total=Count("PT"))
    )
    context = {
        'count_as': count_as,
        'count_an':count_an,
        'count_kp':count_kp,
        'count_kp':count_jd,
        'count_pt':count_pt,
        
    }
    return render(request, "jawapan.html", context)


@login_required(login_url="login")
def quiz_submit(request, quiz_id):
    if request.method == "POST":
        quiz = get_object_or_404(Quiz, id=quiz_id)
        questions = quiz.questions.all()
        error_message = None

        for question in questions:
            choice_id = request.POST.get(f"question_{question.id}", None)
            if choice_id:
                choice = get_object_or_404(Choice, id=choice_id)
                UserResponse.objects.create(
                    user=request.user,
                    quiz=quiz,
                    question=question,
                    selected_choice=choice,
                )
            else:
                error_message = "Select a choice for each questions"

        if error_message:
            messages.error(request, error_message)
            context = {"quiz": quiz, "questions": questions}
            return render(request, "quiz_detail.html", context)

        messages.success(request, "Quiz submitted!")
        return redirect("index_quiz")

    # If method is not POST, redirect to quiz_detail
    return redirect("quiz_detail", quiz_id=quiz_id)
