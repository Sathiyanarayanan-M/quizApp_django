from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.core import serializers
from django.http import HttpResponse
from .models import Questions,QuizModel

# Create your views here.
class QuizView:
    @login_required
    def dashboard(request):
        return render(request,'dashboard.html')

    @user_passes_test(lambda u: (u.is_staff and u.is_active),login_url='restricted_access')
    def admin_console(request):
        if request.user.is_staff:
            return render(request,'admin/staff_console.html')
        else:
            return HttpResponse("<script>alert('Unauthorized Usage'); window.location.href = '/dashboard';</script>")
    
    @user_passes_test(lambda u: (u.is_superuser),login_url='restricted_access')
    def create_staff(request):
        if request.user.is_superuser:
            if request.method == 'POST':
                return HttpResponse('post staff')
            return render(request,'admin/create_staff.html')
        else:
            return HttpResponse("<script>alert('Unauthorized Usage'); window.location.href = '/dashboard';</script>")
   
    @user_passes_test(lambda u: (u.is_active and u.is_staff),login_url='restricted_access')
    def create_quiz(request):
        if request.user.is_staff:
            if request.method == 'POST':
                quiz_name = request.POST['quizname']
                quiz_obj = QuizModel(quiz_name=quiz_name,author=request.user.get_full_name())
                quiz_obj.save()
                for i in range(10):
                    i = str(i)
                    question =  request.POST['question'+ i]
                    option1 = request.POST['question'+i+'option1']
                    option2 = request.POST['question'+i+'option2']
                    option3 = request.POST['question'+i+'option3']
                    option4 = request.POST['question'+i+'option4']
                    correct_answer = request.POST['question'+i+'correct_answer']
                    explanation = request.POST['question'+ i +'explanation']
                    questions_obj = Questions(question=question,option1=option1,option2=option2,option3=option3,option4=option4,answer=correct_answer,explanation=explanation,quiz=quiz_obj)
                    questions_obj.save()
                return HttpResponse("<script>alert('Quiz Updated'); window.location.href = '/staff/quiz-list';</script>")
            else:
                return render(request,'admin/create_quiz.html',{"range":range(10)})
        else:
            return HttpResponse("<script>alert('Unauthorized Usage'); window.location.href = '/dashboard';</script>")
    @user_passes_test(lambda u: (u.is_active and u.is_staff),login_url='restricted_access')
    def quizlist(request):
        return render(request,'admin/quiz_list.html',{"quizzes_list":QuizModel.objects.all()})

    @user_passes_test(lambda u: (u.is_staff and u.is_active) ,login_url='restricted_access')
    def staflist(request):
        return render(request,'admin/staff_list.html')

    @user_passes_test(lambda u: (u.is_active and u.is_staff),login_url='restricted_access')
    def delete_quiz(request,quiz_id):
        QuizModel.objects.get(id=quiz_id).delete()
        return redirect('/staff/quiz-list')

class QuizPlayers:
    def restricted_access(request):
        if request.user.is_active and request.user.is_authenticated:
            if request.user.is_staff:
                return HttpResponse("<script>alert('Unauthorized Usage'); window.location.href = '/staff/';</script>")
            else:
                return HttpResponse("<script>alert('Unauthorized Usage'); window.location.href = '/dashboard/';</script>")
        else:
            return HttpResponse("<script>alert('Unauthorized Usage'); window.location.href = '/login/';</script>")

        