from django.db import models

# Create your models here.

class Quiz(models.Model):
    title = models.CharField(max_length=100)
    is_ready_to_publish = models.BooleanField(default=False)
    

class Question(models.Model):
    title = models.CharField(max_length=255)
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete= models.CASCADE)
    
    def __str__(self):
        return self.title
    
class Choice(models.Model):
    text = models.CharField(max_length=255)
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    score = models.FloatField(default=0)

    def __str__(self) -> str:
        return self.text