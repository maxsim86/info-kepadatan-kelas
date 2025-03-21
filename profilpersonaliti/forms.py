# profilpersonaliti/forms.py

from django import forms

class PersonalDataForm(forms.Form):
    """Form untuk data peribadi."""

    URUSAN_CHOICES = [
        ('1', 'Pilih Urusan 1'),
        ('2', 'Pilih Urusan 2'),
        ('3', 'Pilih Urusan 3'),
    ]

    JANTINA_CHOICES = [
        ('L', 'Lelaki'),
        ('P', 'Perempuan'),
    ]

    WARGANEGARA_CHOICES = [
        ('WNI', 'Warganegara'),
        ('WNA', 'Warga Asing'),
    ]

    AGAMA_CHOICES = [
        ('ISLAM', 'Islam'),
        ('KRISTEN', 'Kristen'),
        ('BUDHA', 'Budha'),
        ('HINDU', 'Hindu'),
        ('LAIN', 'Lain'),
    ]

    BANGSA_CHOICES = [
        ('MELAYU', 'Melayu'),
        ('CINA', 'Cina'),
        ('INDIA', 'India'),
        ('LAIN', 'Lain'),
    ]

    KUMPULAN_PERKHIDMATAN_CHOICES = [
        ('KP1', 'Kumpulan Perkhidmatan 1'),
        ('KP2', 'Kumpulan Perkhidmatan 2'),
        ('KP3', 'Kumpulan Perkhidmatan 3'),
    ]

    KATEGORI_KLIEN_CHOICES = [
        ('KLIEN1', 'Kategori Klien 1'),
        ('KLIEN2', 'Kategori Klien 2'),
        ('KLIEN3', 'Kategori Klien 3'),
    ]
    no_kad_pengenalan = forms.CharField(label='No. Kad Pengenalan', widget=forms.TextInput(attrs={'placeholder': 'Contoh: 880808001111'}))
    nama_penuh = forms.CharField(label='Nama Penuh')
    jantina = forms.ChoiceField(label='Jantina', choices=JANTINA_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    warganegara = forms.ChoiceField(label='Warganegara', choices=WARGANEGARA_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    tarikh_lahir = forms.DateField(label='Tarikh Lahir', widget=forms.DateInput(attrs={'type': 'date'}))
    agama = forms.ChoiceField(label='Agama', choices=AGAMA_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    bangsa = forms.ChoiceField(label='Bangsa', choices=BANGSA_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    kumpulan_perkhidmatan = forms.ChoiceField(label='Kumpulan Perkhidmatan', choices=KUMPULAN_PERKHIDMATAN_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    gred_jawatan = forms.CharField(label='Gred Jawatan')
    jawatan = forms.CharField(label='Jawatan')
    no_telefon_pejabat = forms.CharField(label='No. Telefon Pejabat', widget=forms.TextInput(attrs={'placeholder': 'Contoh: 0368881111'}))
    no_telefon_bimbit = forms.CharField(label='No. Telefon Bimbit', widget=forms.TextInput(attrs={'placeholder': 'Contoh: 0192233445'}))
    alamat_e_mel = forms.EmailField(label='Alamat E-Mel')
    kategori_klien = forms.ChoiceField(label='Kategori Klien', choices=KATEGORI_KLIEN_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    tempat_berkhidmat_pengajian = forms.CharField(label='Tempat Berkhidmat/Pengajian', widget=forms.TextInput(attrs={'placeholder': 'Sila klik butang kemaskini'}))
    urusan = forms.ChoiceField(label='Urusan', choices=URUSAN_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))


**3. Views.py**

```python
# profilpersonaliti/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, Choice, QuizResponse
from .forms import PersonalDataForm  # Impor PersonalDataForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST

def indexQuiz(request):
    quizzes = Quiz.objects.filter(is_ready_to_publish=True)
    context = {"quizzes": quizzes}
    return render(request, "index_quiz.html", context=context)

@login_required(login_url="login")
def quizDetail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    page = request.GET.get("page", 1)
    num_of_items = 10
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
        "page_range": paginator.page_range,
    }
    return render(request, "quiz_detail.html", context)

@require_POST  # Only allow POST requests
def quiz_submit(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    # Get personal data
    personal_form = PersonalDataForm(request.POST)

    if personal_form.is_valid():
        personal_data = personal_form.cleaned_data
    else:
        # Handle invalid personal form data (e.g., show an error)
        messages.error(request, "Please fill in the personal data form correctly.")
        return redirect("quiz_detail", quiz_id=quiz_id)  # Redirect back to quiz

    # Get quiz answers
    response_data = {}
    for question in questions:
        choice_id = request.POST.get(f"question_{question.id}")
        if choice_id:
            response_data[str(question.id)] = int(choice_id)  # Store question ID as string

    # Create QuizResponse
    QuizResponse.objects.create(quiz=quiz, response_data=response_data, personal_data=personal_data)

    return redirect("quiz_thankyou")  # Redirect to thank you page

def quiz_thankyou(request):
    return render(request, "quiz_thankyou.html")

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def quiz_results(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    responses = QuizResponse.objects.filter(quiz=quiz)

    context = {
        'quiz': quiz,
        'responses': responses,
    }

    return render(request, "result.html", context)