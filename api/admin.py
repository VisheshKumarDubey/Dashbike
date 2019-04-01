from django.contrib import admin
from .models import Bike,Booking,BikeModel
# Register your models here.
admin.site.register(Bike)
admin.site.register(Booking)
admin.site.register(BikeModel)