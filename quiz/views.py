from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

class QuizView:
    @login_required
    def dashboard(request):
        return render(request,'dashboard.html')
