from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from .models import User
from django.db import connections
from operator import itemgetter
from module1 import views


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        x = auth.authenticate(email=email, password=password)
        print(x)
        if x is None:
            print("none")
            return redirect('module1:services')
        else:
            print("password incorrect")
            return redirect('module1:home')
    else:
        print('else part')
        return render(request, 'login.html')
    return redirect('module1:gallery')


def register(request):
    context = {}
    if request.method == "POST":
        user = User()
        user.fullname = request.POST['fullname']
        user.phone = request.POST['phone']
        user.email = request.POST['email']
        user.password = request.POST['password']
        if user.fullname == "" or user.phone == "" or user.email == "" or user.password == "":
            messages.info(request, "Some fields are missing")
            return redirect('login')
        else:
            user.save()
    return redirect('login')

