from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import Authentication
from quiz.views import QuizView
urlpatterns = [
    path('',Authentication.index,name='index'),
    path('login/',Authentication.login,name='login'),
    path('logout/',LogoutView.as_view(next_page = 'index'),name='logout'),
    path('registration/',Authentication.registration,name='registration'),
    path('dashboard/',QuizView.dashboard,name='dashboard')
]
