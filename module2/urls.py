from django.urls import path

from . import views

app_name = 'module2'
urlpatterns = [
	path('', views.hotels_list, name="hotels_list"),
	path('flights', views.list1, name="list"),
	path('logout', views.dologout, name="log"),
	path('bookhotel/<int:id>',views.hotel_booking, name="hotel_booking"),
	path('calculate',views.calculate, name="calculate"),
	path('payment',views.payment, name="payment"),
	path('confirmhotel/<int:id>/',views.hotel_confirm, name="hotel_confirm"),
	path('flight_structure/<int:id>',views.flight_structure, name="flight_structure"),
	path('paymentforflight',views.paymentforflight, name="paymentforflight"),
	path('savepayment/<int:id>/<int:seats>/<int:total>',views.savepayment, name="savepayment"),
	path('savehotel/<int:id>/<int:rooms>/<int:total>',views.savehotel, name="savehotel")
]