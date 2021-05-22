from django.urls import path

from . import views
from module2 import views as v
app_name = 'module1'
urlpatterns = [
	path('', views.home, name="home"),
	path('gallery/', views.gallery, name="gallery"),
	path('services/', views.services, name="services"),
	path('contact/', views.contact, name="contact"),
	path('list/', v.list1, name="list"),
	path('hotels_list/', v.hotels_list, name="hotels_list"),
	path('logout/', views.dologout, name="dologout"),
	path('feedback/', views.feedback, name="feedback")
]