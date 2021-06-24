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
                return render(request,'alert.html',{"message":"Password are not Same","url":"/registration"})

            else:
                if User.objects.filter(username = username).exists():
                     return render(request,'alert.html',{"message":"Username is Already Available","url":"/registration"})
                
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
                    if user.is_staff or user.is_superuser:
                        return redirect('staff')
                    return redirect('dashboard')
                else:
                     return render(request,'alert.html',{"message":"Something Went Wrong","url":"/login"})
            else:
                return render(request,'alert.html',{"message":"Invalid Credentials","url":"/login"})
        return render(request,'login.html')
