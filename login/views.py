from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import User
from django.db import connections
from operator import itemgetter
from module1 import views
from django.contrib.auth.models import User,auth


def login(request):
    context = {}
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:

            print(1)
            return redirect('module1:home')
        else:
            messages.error(request,'Invalid Credentials')
            print(2)
            return redirect('login')
    else:
        print(3)
        return render(request, 'login.html', context)


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
            messages.info(request, "Click on Login to start Your Journey")
            user.save()
    return redirect('login')