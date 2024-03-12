from django.contrib import admin
from .models import Quiz, Question, Choice
# Register your models here.


class ChoiceInline(admin.TabularInline):
    model=Choice
    extra =1
    
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_filter = ('quiz',)



admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)
#admin.site.register(Choice)
