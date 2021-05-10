from django.shortcuts import render


def home(request):
    context = {}
    return render(request, 'index.html', context)


def contact(request):
    context = {}
    return render(request, 'contact.html', context)


def services(request):
    context = {}
    return render(request, 'services.html', context)


def gallery(request):
    context = {}
    return render(request, 'gallery.html', context)
