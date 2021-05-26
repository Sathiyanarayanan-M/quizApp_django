from django.db import models
from django.db.models.constraints import CheckConstraint
from django.db.models.fields import CharField

# Create your models here.

class QuizModel(models.Model):
    quiz_name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.quiz_name


class Questions(models.Model):
    question = models.CharField(max_length=200)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    answer = models.CharField(max_length=7)
    explanation = models.CharField(max_length=200)
    quiz = models.ForeignKey(QuizModel,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.question

    

