from django.shortcuts import render
from django.http import HttpResponse
from pyfcm import FCMNotification
from Users.models import CustomUser
from api.models import Booking
# Create your views here.
import json
from django.http import StreamingHttpResponse


def fcm_insert(request,pk):
    token=request.GET.get('fcm_token','')
    a=CustomUser.objects.filter(id=pk).update(fcm_token=token)
    print(a)
    return HttpResponse(token)


def send_notifications(request): #the method which sends the notification
    #received_json_data = json.loads(request.body.decode("utf-8"))
	path_to_fcm = "https://fcm.googleapis.com"
	server_key = 'AAAAzhLjAdI:APA91bFgn-4PLcHtcPaX4H3EdM2MyyCOb7mHgIUNQISdmJlUoI_hm4suFKPVStcjCoYwQiftypmsJXYNlRo-4S5pPnFmLQrPBEn7-K0D2sWQHmc0abbZdOApSrh16LqbpjOrJ7QIISsx'
	reg_id = request.GET.get('to_token','')#'cTksz72F6uU:APA91bEKsq_oCyqHX6rk3Ne6-KWFfMSdecmLVy7zKUqHLjaCwybC4tF1e9uVhRsFC00fyFKCV3z8JGhWYxVFx4paMkE8REe8f4JNxBcNi2TseF04JhEl7MJnb0M6Qk60n83NFwf8I9g0'#CustomUser.objects.all()[4].fcm_token #quick and dirty way to get that ONE fcmId from table
	message_title =request.GET.get('title','')
	message_body = request.GET.get('body','')
	result = FCMNotification(api_key=server_key).notify_single_device(registration_id=reg_id, message_title=message_title, message_body=message_body)
	return HttpResponse(result)


	#in case you wanna send notifications to multitple ids in just replace the argument registration_id in the notify_single_device
#function with registration_ids and provide it with the list of ids you wanna send notifications to.