from django.db import models
#from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.


class Quiz(models.Model):
    title = models.CharField(max_length=100)
    is_ready_to_publish = models.BooleanField(default=False)

    def __str__(self):
        return self.title


# Soalan untuk kuiz
class Question(models.Model):
    text = models.CharField(max_length=255)
    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
    question_number = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['text']



class Choice(models.Model):
    text = models.CharField(max_length=255)
    question = models.ForeignKey(
        Question, related_name="choices", on_delete=models.CASCADE
    )
    score = models.FloatField(default=0)

    def __str__(self) -> str:
        return self.text


class UserResponse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user.username}'s response to {self.question.text} in {self.quiz.title} is {self.selected_choice.text}"

    def score(self):
        return self.selected_choice.score if self.selected_choice else 0

    # mengira jumlah score
    def calculate_score(self):
        total_score = sum(choice.score for choice in self.question.choice.all())
        return total_score


