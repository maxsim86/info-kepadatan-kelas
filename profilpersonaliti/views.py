from django.shortcuts import render, get_object_or_404, redirect
from profilpersonaliti.models import Quiz, Question, Choice, UserResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.db.models import Sum


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
    question_numbers = [1, 13, 25, 37, 49, 61, 73]

    count_per_question = {}
    for number in question_numbers:
        count_per_question[number] = (
            UserResponse.objects.filter(
                quiz_id=quiz_id, question__question_number=number
            )
            .values("selected_choice")
            .annotate(total_score=Sum("selected_choice__score"))
            .order_by("selected_choice")
        )

        total_sum = sum(choice["total_score"] for choices in count_per_question.values() for choice in choices)

    context = {
        "count_per_question": count_per_question,
        "total_sum": total_sum,
    }
    return context


# Quiz submit
@login_required(login_url="login")
def quiz_submit(request, quiz_id):
    if request.method == "POST":
        quiz = get_object_or_404(Quiz, id=quiz_id)
        questions = quiz.questions.all()
        error_message = None

        # Simpan result user
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

        # menampilkan hasil di result.html
        count_context = count_choices(request, quiz_id)
        return render(request, "result.html", count_context)

        # messages.success(request, "Quiz submitted!")
        # return redirect("index_quiz")

    # If method is not POST, redirect to quiz_detail
    return redirect("quiz_detail", quiz_id=quiz_id)
