from django.shortcuts import render
from django.http import HttpResponse
from pyfcm import FCMNotification
from Users.models import *
from api.models import Booking
from django.conf import settings
import json
from django.http import StreamingHttpResponse


def fcm_insert(request, pk):
    token = request.GET.get('fcm_token', '')
    user_type = request.GET.get('user_type', '')
    if user_type == 'client':
        a = CustomUser.objects.filter(
            username=ClientDetail.objects.get(id=pk)).update(fcm_token=token)
    if user_type == 'dealer':
        a = CustomUser.objects.filter(
            username=DealerDetail.objects.get(id=pk)).update(fcm_token=token)
    return HttpResponse(token)


'''

		We have to create a view  which checks for fcm token, 
		if there is no fcm token it returns false else it returns true

'''


def send_notifications(request, pk):  # the method which sends the notification
    if(str(request.GET.get('user_type', '')) == 'client'):
        reg_id = CustomUser.objects.get(
            username=ClientDetail.objects.get(id=pk)).fcm_token
    if(str(request.GET.get('user_type', '')) == 'dealer'):
        reg_id = CustomUser.objects.get(
            username=DealerDetail.objects.get(id=pk)).fcm_token
    message_title = request.GET.get('title', '')
    message_body = request.GET.get('body', '')
    result = FCMNotification(api_key=settings.FCM_SERVER_KEY).notify_single_device(
        registration_id=reg_id, message_title=message_title, message_body=message_body)
    return HttpResponse(result)

    # in case you wanna send notifications to multitple ids in just replace the argument registration_id in the notify_single_device
# function with registration_ids and provide it with the list of ids you wanna send notifications to.
