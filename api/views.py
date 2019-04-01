from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Bike, Booking, BikeModel
from api.serializers import *
from rest_framework import generics
from api.permissions import IsOwnerOrReadOnly,IsAdminUserOrReadOnly
from rest_framework import permissions, exceptions
from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from Users.models import DealerDetail
from django.conf import settings
from . import locations

from django.db import models
from django.db.models.expressions import RawSQL
from rest_framework.exceptions import APIException


class BikeModelList(generics.ListCreateAPIView):
    queryset = BikeModel.objects.all()
    print('hey0')
    serializer_class = BikeModelSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self, *args, **kwargs):
        print('hey1')
        if self.request.user.user_type == 'Dealer':
            print('hey')
            return BikeModel.objects.filter(dealer=DealerDetail.objects.get(type=self.request.user))
        else:
            value = BikeModel.objects.filter(dealer=self.kwargs['id'],bike_isAvailable=True)
            if value:
                return value
            else:
                raise APIException("Not Found!")


class BikeModelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BikeModel.objects.filter()
    serializer_class = BikeModelSerializer
    permission_classes = [IsOwnerOrReadOnly,
                          permissions.IsAuthenticated, ]


class DealerList(generics.ListAPIView):
    def get_queryset(self, *args, **kwargs):
        if(settings.NEARBY_SHOPS):
            if self.request.user.user_type == 'Dealer':
                return locations.get_location_nearby_coords(float(self.kwargs['lat']), float(self.kwargs['lon']))
            else:
                return locations.get_location_nearby_coords(float(self.kwargs['lat']), float(self.kwargs['lon'])).filter(has_bike=True)
        else:
            if self.request.user.user_type == 'Dealer':
                return DealerDetail.objects.all()
            else:
                return DealerDetail.objects.filter(has_bike=True)
    serializer_class = DealerDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


class BikeList(generics.ListCreateAPIView):
    queryset = Bike.objects.all()
    serializer_class = BikeSerializer
    permission_classes = [IsAdminUserOrReadOnly, ]


class BikeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bike.objects.all()
    serializer_class = BikeSerializer
    permission_classes = [IsAdminUserOrReadOnly, ]
    

class BookingList(generics.ListCreateAPIView):
    #queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    def get_queryset(self, *args, **kwargs):
        if self.request.user.user_type == 'Dealer':
            return Booking.objects.filter(dealer=DealerDetail.objects.get(type=self.request.user))
        else:
            value = Booking.objects.filter(client=ClientDetail.objects.get(type=self.request.user))
            if value:
                return value
            else:
                raise APIException("Not Found!")


class BookingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, ]

