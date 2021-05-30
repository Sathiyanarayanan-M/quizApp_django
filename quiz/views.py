from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Questions, QuizModel, UserResult
from django.contrib.auth import get_user_model

# Create your views here.
class QuizView:
    @login_required
    def dashboard(request):
        quiz_ids = {
            quiz.quiz_id: quiz.score
            for quiz in UserResult.objects.filter(user=request.user.username)
        }
        quiz_scores = list(quiz_ids.values())
        quiz_names = [
            QuizModel.objects.get(id=int(ids)).quiz_name
            for ids in list(quiz_ids.keys())
        ]
        played_quizzes = dict(zip(quiz_names, quiz_scores))
        return render(
            request, "dashboard.html", {"played_quizzes": played_quizzes.items()}
        )

    @user_passes_test(
        lambda u: (u.is_staff and u.is_active), login_url="restricted_access"
    )
    def admin_console(request):
        return render(request, "admin/staff_console.html")

    @user_passes_test(lambda u: (u.is_superuser), login_url="restricted_access")
    def create_staff(request):
        if request.method == "POST":
            f_name = request.POST["f_name"]
            l_name = request.POST["l_name"]
            username = request.POST["username"]
            email = request.POST["email"]
            password = request.POST["password"]
            c_password = request.POST["c_password"]
            print(f_name,l_name,username,email,password,c_password)
            if password != c_password:
                return render(request,'alert.html',{"message":"The Password are not Same","url":"/staff/create-staff/"})
                
            else:
                if User.objects.filter(username=username).exists():
                    return render(request,'alert.html',{"message":"User Already Available","url":"/staff/create-staff/"})
                else:
                    create_staff = User.objects.create_user(
                        username=username,
                        password=password,
                        email=email,
                        first_name=f_name,
                        last_name=l_name,
                        is_staff=True,
                    )
                    create_staff.save()
                    return redirect("/staff/staff-list/")
        return render(request, "admin/create_staff.html")
    @user_passes_test(
        lambda u: (u.is_active and u.is_staff), login_url="restricted_access"
    )
    def create_quiz(request):
        if request.method == "POST":
            quiz_name = request.POST["quizname"]
            quiz_obj = QuizModel(
                quiz_name=quiz_name, author=request.user.get_full_name()
            )
            quiz_obj.save()
            for i in range(10):
                i = str(i)
                question = request.POST["question" + i]
                option1 = request.POST["question" + i + "option1"]
                option2 = request.POST["question" + i + "option2"]
                option3 = request.POST["question" + i + "option3"]
                option4 = request.POST["question" + i + "option4"]
                correct_answer = request.POST["question" + i + "correct_answer"]
                explanation = request.POST["question" + i + "explanation"]
                questions_obj = Questions(
                    question=question,
                    option1=option1,
                    option2=option2,
                    option3=option3,
                    option4=option4,
                    answer=correct_answer,
                    explanation=explanation,
                    quiz=quiz_obj,
                )
                questions_obj.save()
            return render(request,'alert.html',{"message":"Quiz Updated","url":"/staff/quiz-list"})
        else:
            return render(request, "admin/create_quiz.html", {"range": range(10)})

    @user_passes_test(
        lambda u: (u.is_active and u.is_staff), login_url="restricted_access"
    )
    def quizlist(request):
        return render(
            request, "admin/quiz_list.html", {"quizzes_list": QuizModel.objects.all()}
        )

    @user_passes_test(
        lambda u: (u.is_staff and u.is_active), login_url="restricted_access"
    )
    def staflist(request):
        staffs = get_user_model().objects.filter(is_staff=True)
        users = get_user_model().objects.filter(is_staff=False)
        return render(request, "admin/staff_list.html",{"staffs":staffs,"users":users})

    @user_passes_test(
        lambda u: (u.is_active and u.is_staff), login_url="restricted_access"
    )
    def delete_quiz(request, quiz_id):
        QuizModel.objects.get(id=quiz_id).delete()
        return redirect("/staff/quiz-list")


class QuizPlayers:
    @login_required
    def play_quiz(request, quiz_id, qn_no):
        all_q = Questions.objects.filter(quiz_id=int(quiz_id))
        if request.method == "POST":
            qn_no = int(request.POST["qn_no"]) + 1
            if qn_no in range(0, 10):
                question_obj = all_q[int(qn_no)]
                answer_choosed = request.POST["result"]
                if UserResult.objects.filter(
                    user=request.user.username, quiz_id=quiz_id
                ).exists():
                    if answer_choosed == "correct":
                        u = UserResult.objects.get(
                            user=request.user.username, quiz_id=quiz_id
                        )
                        u.score = str(int(u.score) + 1)
                        u.save()
                        return render(
                            request,
                            "student/play_quiz.html",
                            {
                                "question_obj": question_obj,
                                "qn_no": int(qn_no),
                                "quiz_id": quiz_id,
                            },
                        )
                    else:
                        return render(
                            request,
                            "student/play_quiz.html",
                            {
                                "question_obj": question_obj,
                                "qn_no": int(qn_no),
                                "quiz_id": quiz_id,
                            },
                        )
                else:
                    if answer_choosed == "correct":
                        u = UserResult(
                            user=request.user.username, quiz_id=quiz_id, score=1
                        )
                        u.save()
                        return render(
                            request,
                            "student/play_quiz.html",
                            {
                                "question_obj": question_obj,
                                "qn_no": int(qn_no),
                                "quiz_id": quiz_id,
                            },
                        )
                    else:
                        u = UserResult(
                            user=request.user.username, quiz_id=quiz_id, score=0
                        )
                        u.save()
                        return render(
                            request,
                            "student/play_quiz.html",
                            {
                                "question_obj": question_obj,
                                "qn_no": int(qn_no),
                                "quiz_id": quiz_id,
                            },
                        )
            else:
                if UserResult.objects.filter(
                    user=request.user.username, quiz_id=quiz_id
                ).exists():
                    score = UserResult.objects.get(
                        user=request.user.username, quiz_id=quiz_id
                    ).score
                    return render(request,'alert.html',{"message":"Your Score"+score,"url":"/user/quizzes/"})
                else:
                    return render(request,'alert.html',{"message":"Something Went Wrong","url":"/user/quizzes"})
        else:
            question_obj = all_q[0]
            if UserResult.objects.filter(
                user=request.user.username, quiz_id=quiz_id
            ).exists():
                u = UserResult.objects.get(user=request.user.username, quiz_id=quiz_id)
                u.score = "0"
                u.save()
                return render(
                    request,
                    "student/play_quiz.html",
                    {
                        "question_obj": question_obj,
                        "qn_no": int(qn_no),
                        "quiz_id": quiz_id,
                    },
                )
            return render(
                request,
                "student/play_quiz.html",
                {"question_obj": question_obj, "qn_no": int(qn_no), "quiz_id": quiz_id},
            )

    @login_required
    def student_quizzes(request):
        return render(
            request,
            "student/student_quizzes.html",
            {"quizzes": QuizModel.objects.all()},
        )

    def restricted_access(request):
        if request.user.is_active and request.user.is_authenticated:
            if request.user.is_staff:
                return redirect("/staff/")
            else:
                return redirect("/dashboard/")
        else:
            return render(request,'alert.html',{"message":"Unauthorized Usage","url":"/login"})
