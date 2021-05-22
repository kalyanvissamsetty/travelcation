from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail,EmailMultiAlternatives
from django.utils.html import strip_tags
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



def home(request):
    return render(request, 'index.html')


@login_required(login_url='initial:register')
def contact(request):
    u = request.session['uname']
    return render(request, 'contact.html',{'u':u})


@login_required(login_url='initial:register')
def services(request):
    u = request.session['uname']
    return render(request, 'services.html',{'u':u})


@login_required(login_url='initial:register')
def gallery(request):
    u = request.session['uname']
    return render(request, 'gallery.html',{'u':u})


@login_required(login_url='initial:register')
def dologout(request):
    try:
        logout(request)
        del request.session['uname']
        return redirect('initial:login')
    except KeyError:
        pass
    return redirect('initial:register')



@login_required(login_url='initial:register')
def feedback(request):
    name = request.POST['name']
    phone = request.POST['phone']
    email = request.POST['email']
    feedback = request.POST['feedback']
    html_content = render_to_string("emial_template.html",{'title': 'Travelcation Feedback', 'fullname': name})
    text_content = strip_tags(html_content)
    subject = 'Thank You for Submitting Your Review'
    email = EmailMultiAlternatives(
        subject, text_content, settings.EMAIL_HOST_USER, [email]
    )
    email.attach_alternative(html_content,"text/html")
    email.send()
    return render(request, 'contact.html')
