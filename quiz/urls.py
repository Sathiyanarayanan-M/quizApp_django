from django.urls import path
from .views import QuizView

urlpatterns = [
    path('',QuizView.admin_console,name='staff'),
    path('create-staff/',QuizView.create_staff,name='create-staff'),
    path('create-quiz/',QuizView.create_quiz,name='create-quiz'),
    path('quiz-list/',QuizView.quizlist,name='quiz-list'),
    path('staff-list/',QuizView.staflist,name='staff-list'),
    path('delete-quiz/<str:quiz_id>/',QuizView.delete_quiz,name='delete-quiz'),
]
