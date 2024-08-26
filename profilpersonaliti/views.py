from django.shortcuts import render, get_object_or_404, redirect
from profilpersonaliti.models import Quiz, Question, Choice, UserResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# from django.db.models import Count


# Create your views here.
def indexQuiz(request):
    quizzes = Quiz.objects.filter(is_ready_to_publish=True)
    context = {"quizzes": quizzes}
    return render(request, "index_quiz.html", context=context)


# quiz detail(soalan quiz)
@login_required(login_url="login")
def quizDetail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    # setup pagination
    page = request.GET.get("page")
    num_of_items = 3
    paginator = Paginator(questions, num_of_items)  # show 5 question for question

    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        questions = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        questions = paginator.page(page)

    context = {
        "quiz": quiz,
        "questions": questions,
        "Paginator": paginator,
    }
    return render(request, "quiz_detail.html", context)


# submit quiz and calculate total score  base on AS, AN, KD, KP, JD, PT, SB,
# PN,PN, IG, PM, KC, KS


# bahagian 3 : borang jawapan dengan nilai serta jadual score dan pemeratusan %
def count_choices(request, quiz_id):
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
            user_responses = UserResponse.objects.filter(
                quiz_id=quiz_id, question__question_number=number
            )
            score_sum = sum(user_response.score() for user_response in user_responses)

            group_data[number] = {
                "user_responses": user_responses,
                "score_sum": score_sum,
            }
            total_sum += score_sum
            total_group_score += score_sum

        group_data["total_group_score"] = total_group_score
        count_per_question[group_name] = group_data

    context = {
        "count_per_question": count_per_question,
        "total_sum": total_sum,
    }

    return context


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


@login_required(login_url="login")
def score_percentage(request, quiz_id):
    # calculate total score for each group name
    total_count = count_choices(request, quiz_id)
    total_scores = {
        group_name: data["total_group_score"]
        for group_name, data in total_count["count_per_question"].items()
    }

    # Map total scores to percentage values
    score_percentages = {
        group_name: percentage_values.get(total_score, 0)
        for group_name, total_score in total_scores.items()
    }


# Render templates to print display score percentage
#    context = {"score_percentages": score_percentages}
#    return render(request, "score_percentage.html", context)


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
                error_message = "Pilih satu untuk setiap pertanyaan"

        if error_message:
            messages.error(request, error_message)
            context = {"quiz": quiz, "questions": questions}
            return render(request, "quiz_detail.html", context)

        # total_score_sum = calculate_score_sum(request, quiz_id)

        # menampilkan hasil di result.html
        count_context = count_choices(request, quiz_id)

        return render(
            request,
            "result.html",
            {
                **count_context,
            },
        )

        # messages.success(request, "Quiz submitted!")
        # return redirect("index_quiz")

    # If method is not POST, redirect to quiz_detail
    return redirect("quiz_detail", quiz_id=quiz_id)
