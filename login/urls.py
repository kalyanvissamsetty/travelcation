from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
app_name = 'initial'
urlpatterns = [
	path('', views.registerPage, name="register"),
	path('login', views.loginPage, name="login"),
	path('logout', views.logoutUser, name="logout"),
	path('profile', views.profile, name="profile"),
	path('test', views.test, name="test"),
]