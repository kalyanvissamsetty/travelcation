from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from .models import User
from django.template import RequestContext
from django.db import connections
from operator import itemgetter
# from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail,EmailMultiAlternatives
from django.utils.html import strip_tags
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth import authenticate, login, logout
from module2.models import SaveFlight,SaveHotel


def test(request):
    if request.method == 'POST':
        u = request.POST.get('ido')
        print(u)
        return render(request,'testing.html')
    return render(request, 'testing.html')




def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            SaveFlight.objects.filter(uname=request.session['uname']).update(uname=u_form.cleaned_data.get('username'))
            SaveHotel.objects.filter(uname=request.session['uname']).update(uname=u_form.cleaned_data.get('username'))
            u_form.save()
            request.session['uname'] = u_form.cleaned_data.get('username')
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('initial:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    obj = SaveFlight.objects.filter(uname=request.session['uname'])
    hotels = SaveHotel.objects.filter(uname=request.session['uname'])
    print(len(obj))
    print(len(hotels))
    li1 = []
    fl = False
    hl = False
    all = False
    if len(obj) > 0:
        fl = True
    if len(hotels) > 0:
        hl = True
    if len(obj) == 0 and len(hotels) == 0:
        all =True


    for i in hotels:
        details = {
            'city': i.city,
            'name': i.name,
            'img': i.img,
            'price': i.price,
            'rooms': i.rooms,
            'cardno': i.cardno,
            'totalprice': i.totalprice
        }
        li1.append(details)
    li = []
    for i in obj:
        details = {
            'source': i.source,
            'destination': i.destination,
            'flight_name': i.flight_name,
            'flight_id': i.flight_id,
            'departure': i.departure,
            'arrival': i.arrival,
            'price': i.price,
            'cardno':i.cardno,
            'seats':i.seats,
            'totalprice': i.totalprice
        }
        li.append(details)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'li':li,
        'li1':li1,
        'a1':fl,
        'b1':hl,
        'all':all
    }

    return render(request,'profile.html',context)


def registerPage(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        ctx = {'form': form}
        if form.is_valid():
            form.save()

            phone = form.cleaned_data.get('phone')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            request.session['uname'] = username
            request.session['email'] = email
            request.session['phone'] = phone
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            html_content = render_to_string("email_template.html",
                                            {'title': 'Travelcation Registration', 'username': username})
            text_content = strip_tags(html_content)
            subject = 'Welcome to Travelcation Groups, Start your Safe and Wonderful journey with us'
            email = EmailMultiAlternatives(
                subject, text_content, settings.EMAIL_HOST_USER, [email]
            )
            email.attach_alternative(html_content,"text/html")
            email.send()
            messages.success(request, f'Account created for {username}!')
            return redirect('module1:home')
    else:
        form = UserRegisterForm()
        ctx = {'form': form}
    return render(request, 'register.html', {'form': form})




def loginPage(request):
    print('heloo')
    print(request.user.is_authenticated)
    if request.user.is_authenticated:
        return redirect('module1:home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            print(username)
            print('hi')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                request.session['uname'] = username
                login(request, user)
                return redirect('module1:home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'register.html', context)
    return render(request, 'register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('initial:register')

# def loginPage(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         print(username,password)
#         print(1)
#         # user = authenticate(request,email=email, password=password)
#         try:
#             u = User.objects.get(username=username, password=password)
#             request.session['uname'] = username
#             print("loggedin")
#             return redirect('module1:home')
#         except:
#             u = None
#             messages.info(request, 'Email or Password is incorrect')
#             return redirect('initial:login')
#     else:
#         print('else part')
#         context = {}
#         return render(request, 'register.html',context)
#     return redirect('initial:login')


# def registerPage(request):
#     context = {}
#     if request.method == "POST":
#         user = User()
#         user.username = request.POST['username']
#         user.phone = request.POST['phone']
#         user.email = request.POST['email']
#         user.password = request.POST['password']
#         if user.username == "" or user.phone == "" or user.email == "" or user.password == "":
#             messages.info(request, "Some fields are missing")
#             return redirect('initial:login')
#         else:
#             user.save()
#             html_content = render_to_string("email_template.html",{'title': 'Travelcation Registration', 'username': user.username})
#             text_content = strip_tags(html_content)
#             subject = 'Welcome to Travelcation Groups, Start your Safe and Wonderful journey with us'
#             email = EmailMultiAlternatives(
#                 subject, text_content, settings.EMAIL_HOST_USER, [user.email]
#             )
#             email.attach_alternative(html_content,"text/html")
#             email.send()
#             request.session['uname'] = user.username
#             return redirect('module1:home')
#     return redirect('initial:login')
#
