from django.urls import path

from . import views

app_name = 'module1'
urlpatterns = [

	path('', views.home, name="home"),
	path('gallery/', views.gallery, name="gallery"),
	path('services/', views.services, name="services"),
	path('contact/', views.contact, name="contact"),

]