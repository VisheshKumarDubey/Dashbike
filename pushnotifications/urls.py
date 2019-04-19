from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
	#path('', views.homePageView, name='home'), #the home page
	path(r'insert/<int:pk>/', views.fcm_insert, name='insert'), #the address targetted at the MainActivity.java file. It was the destination where Volley has to send data
	path(r'send/<int:pk>/', views.send_notifications, name='send') #for sending the notification
]