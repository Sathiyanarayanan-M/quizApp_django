from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,decorators
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse

class Authentication:

    def index(request):
        return render(request,'home.html')

    def registration(request):
        if  request.method == 'POST':
            f_name = request.POST['f_name']
            l_name = request.POST['l_name']
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            c_password = request.POST['c_password']
            if password != c_password:
                return HttpResponse(
                "<script>alert('The passwords aren't same'); window.location.href = '/registration';</script>"
            )
            else:
                if User.objects.filter(username = username).exists():
                    return HttpResponse(
                    "<script>alert('User already available'); window.location.href = '/registration';</script>"
                )
                else:
                    create_user =  User.objects.create_user( username = username, password = password,email = email,first_name=f_name,last_name=l_name)
                    create_user.save()
                    return redirect("login")
        return render(request,'registration.html')
    def login(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request,username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('dashboard')
                else:
                    return HttpResponse( "<script>alert('Something went Wrong'); window.location.href = '/login';</script>")
            else:
                return HttpResponse( "<script>alert('Invalid Credential'); window.location.href = '/login';</script>")

        return render(request,'login.html')
