from django.db import models

# Create your models here.
from django.contrib.auth.models import User

# class Conversation(models.Model):
#     participants = models.ManyToManyField(User, related_name='conversation')
#     created_add = models.DateTimeField(auto_now_add=True)

# class Message(models.Model):
#     conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
#     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
#     content = models.TextField()