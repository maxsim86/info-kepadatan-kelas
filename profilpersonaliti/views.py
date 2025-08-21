from django.shortcuts import render, get_object_or_404, redirect
from profilpersonaliti.models import Quiz, Choice, QuizResponse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from .forms import PersonalDataForm


# from django.db.models import Count


# Create your views here.
def indexQuiz(request):
    quizzes = Quiz.objects.filter(is_ready_to_publish=True)
    personal_form = PersonalDataForm()
    context = {
        "quizzes": quizzes,
        "personal_form": personal_form,
    }
    return render(request, "index_quiz.html", context=context)


# quiz detail(detail quiz)
def quizDetail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all().order_by("question_number")
    page = request.GET.get("page", 1)
    num_of_items = 93
    paginator = Paginator(questions, num_of_items)
    try:
        questions_page = paginator.page(page)
    except PageNotAnInteger:
        questions_page = paginator.page(1)
    except EmptyPage:
        questions_page = paginator.page(paginator.num_pages)
    offset = (questions_page.number - 1) * num_of_items
    context = {
        "quiz": quiz,
        "questions": questions_page,
        "offset": offset,
    }
    return render(request, "quiz_detail.html", context)


# submit quiz and calculate total score  base on AS, AN, KD, KP, JD, PT, SB,
# PN,PN, IG, PM, KC, KS


# bahagian 3 : borang jawapan dengan nilai serta jadual score dan peratus %
def count_choices(quiz_response):
    question_numbers = {
        "AS": [1, 13, 25, 37, 49, 61, 73],
        "AN": [2, 14, 26, 38, 50, 62, 74, 85],
        "KD": [3, 15, 27, 39, 51, 63, 75, 86],
        "KP": [4, 16, 28, 40, 52, 64, 76, 87],
        "JD": [5, 17, 29, 41, 53, 65, 77],
        "PT": [6, 18, 30, 42, 54, 66, 78, 88],
        "SB": [7, 19, 31, 43, 55, 67, 79, 89],
        "PN": [8, 20, 32, 44, 56, 68, 80, 90],
        "IG": [9, 21, 33, 45, 57, 69, 81],
        "PM": [10, 22, 34, 46, 58, 70, 82],
        "KC": [11, 23, 35, 47, 59, 71, 83, 91, 93],
        "KS": [12, 24, 36, 48, 60, 72, 84, 92],
    }

    count_per_question = {}
    total_sum = 0

    for group_name, numbers in question_numbers.items():
        group_data = {}
        total_group_score = 0
        for number in numbers:
            question = Question.objects.get(
                quiz=quiz_response.quiz, question_number=number
            )
            choice_id = quiz_response.response_data.get(str(question.id))
            score_sum = 0
            if choice_id:
                choice = Choice.objects.get(id=choice_id)
                score_sum = choice.score
            group_data[number] = {"score_sum": score_sum}
            total_sum += score_sum
            total_group_score += score_sum
        group_data["total_group_score"] = total_group_score
        count_per_question[group_name] = group_data
    return {"count_per_question": count_per_question, "total_sum": total_sum}


percentage_values = {
    0: 0,
    1: 5,
    2: 9,
    3: 14,
    4: 19,
    5: 24,
    6: 28,
    7: 33,
    8: 38,
    9: 43,
    10: 48,
    11: 55,
    12: 57,
    13: 62,
    14: 67,
    15: 71,
    16: 76,
    17: 81,
    18: 86,
    19: 90,
    20: 95,
    21: 99,
}


def score_percentage(quiz_response):
    total_count = count_choices(quiz_response)
    total_scores = {
        group_name: data["total_group_score"]
        for group_name, data in total_count["count_per_question"].items()
    }
    score_percentages = {
        group_name: percentage_values.get(total_score, 0)
        for group_name, total_score in total_scores.items()
    }
    score_categories = {
        group_name: calculate_score_percentage(percentage)
        for group_name, percentage in score_percentages.items()
    }
    return {
        "score_percentages": score_percentages,
        "score_categories": score_categories,
    }


def calculate_percentage(total, jn):
    percentage = 0
    return percentage


def calculate_score_percentage(percentage):
    # determine the score category base on the percentage
    if percentage <= 20:
        return "RENDAH"
    elif 20 < percentage <= 40:
        return "SEDERHANA RENDAH"
    elif 40 < percentage <= 60:
        return "SEDERHANA"
    elif 60 < percentage <= 80:
        return "SEDERHANA TINGGI"
    else:
        return "TINGGI"


# Bahagian 4 : Jadual score dan pemeratusan
def jadual_score_percentage(request):
    totals = {
        "AS": 15,
        "AN": 10,
        "KD": 12,
    }
    jn = {
        "AS": [
            0,
            5,
            9,
            14,
            19,
            24,
            28,
            33,
            38,
            43,
            48,
            55,
            57,
            62,
            67,
            71,
            76,
            81,
            86,
            90,
            95,
            99,
        ],
        "AN": [
            0,
            4,
            8,
            12,
            17,
            21,
            25,
            29,
            33,
            37,
            42,
            46,
            50,
            54,
            58,
            62,
            71,
            75,
            79,
            83,
            87,
            92,
            96,
            99,
        ],
        "KD": [
            0,
            4,
            8,
            12,
            17,
            21,
            25,
            29,
            33,
            37,
            42,
            46,
            50,
            54,
            58,
            62,
            67,
            71,
            75,
            79,
            83,
            87,
            92,
            96,
            99,
        ],
    }

    percentage_dict = {}

    for group_name, total in totals.items():
        percentage = calculate_percentage(total, jn[group_name])
        category = calculate_score_percentage(percentage)
        percentage_dict[group_name] = {"percentage": percentage, "category": category}

    return render(
        request, "jadual_score_percentage.html", {"percentage_dict": percentage_dict}
    )


@require_POST
def quiz_submit(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    personal_form = PersonalDataForm(request.POST)

    # Validasi formulir data pribadi
    if not personal_form.is_valid():
        messages.error(request, "Silakan isi formulir data pribadi dengan benar.")
        return redirect("quiz_detail", quiz_id=quiz_id)

    personal_data = personal_form.cleaned_data

    # Validasi jawaban kuis
    all_questions_answered = True
    response_data = {}
    for question in questions:
        choice_id = request.POST.get(f"question_{question.id}", None)
        if not choice_id:
            all_questions_answered = False
            break
        response_data[str(question.id)] = int(choice_id)

    if not all_questions_answered:
        messages.error(request, "Silakan jawab semua pertanyaan sebelum hantar.")
        return redirect("quiz_detail", quiz_id=quiz_id)

    # Simpan data ke QuizResponse
    QuizResponse.objects.create(
        quiz=quiz,
        response_data=response_data,
        personal_data=personal_data,
    )

    # Kirim data ke result.html
    context = {
        "quiz": quiz,
        "responses": QuizResponse.objects.filter(
            quiz=quiz, response_data=response_data, personal_data=personal_data
        ),
    }

    return render(request, "result.html", context)
