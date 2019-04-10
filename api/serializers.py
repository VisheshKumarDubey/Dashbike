from rest_framework import serializers
from api.models import *
from Users.models import *
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import APIException

class BikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = '__all__'
        read_only_fields = ('thumbnail', )
        # depth=1

class BikeModelSerializer(serializers.ModelSerializer):
    bike_img = serializers.ImageField(read_only=True)
    thumbnail = serializers.ImageField(read_only=True)
    bike_model = serializers.CharField()
    dealer = serializers.CharField(read_only=True)
    bike_model_id=serializers.CharField(read_only=True)

    class Meta:
        model = BikeModel
        fields = ('id', "bike_model",'bike_model_id', 'dealer', 'description', 'count', 'bike_rate_hr',
                  'bike_rate_h', 'bike_rate_f', "bike_img", 'bike_isAvailable', 'thumbnail')
        read_only_fields = ('is_active', 'dealer')
        extra_kwargs = {'count': {'required': True}}

    def create(self, validated_data):
        if(self.context['request'].user.user_type == 'Dealer'):
            return BikeModel.objects.create(dealer=DealerDetail.objects.get(type=self.context['request'].user),
                                            bike_model=Bike.objects.get(bike_name=validated_data.get(
                                                'bike_model')),
                                            description=validated_data.get(
                'description'),
                count=validated_data.get('count'),
                bike_rate_hr=validated_data.get(
                'bike_rate_hr'),
                bike_rate_h=validated_data.get(
                'bike_rate_h'),
                bike_rate_f=validated_data.get(
                'bike_rate_f'),
                bike_isAvailable=validated_data.get('bike_isAvailable'))
        else:
            raise APIException("Client can not add Bike!")

    def update(self, instance, validated_data):
        instance.description = validated_data.get(
            'description', instance.description)
        instance.bike_model = validated_data.get(
            'bike_model', instance.bike_model)
        instance.count = validated_data.get('count', instance.count)
        instance.bike_rate_hr = validated_data.get(
            'bike_rate_hr', instance.bike_rate_hr)
        instance.bike_rate_h = validated_data.get(
            'bike_rate_h', instance.bike_rate_h)
        instance.bike_rate_f = validated_data.get(
            'bike_rate_f', instance.bike_rate_f)
        instance.bike_isAvailable = validated_data.get(
            'bike_isAvailable', instance.bike_isAvailable)
        #instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance

class BookingSerializer(serializers.ModelSerializer):
    dealer_name=serializers.CharField(read_only=True)
    bike_model_name=serializers.CharField(read_only=True)
    booking_status = (
        ('cancelled', 'cancelled'),
        ('failed', 'failed'),
        ('booked', 'booked'),
        ('pending', 'pending'),
    )
    status = serializers.ChoiceField(choices=booking_status,
        style={'base_template': 'radio.html'},
        required=True)
    unit_duration = (
        ('hrs', 'hrs'),
        ('half_day', 'half_day'),
        ('full_day', 'full_day'),
    )
    duration_unit = serializers.ChoiceField(choices=unit_duration,
        style={'base_template': 'radio.html'},
        required=True)
    class Meta:
        model = Booking
        fields = ('id','dealer','dealer_name', 'bike_model','bike_model_name', 'pickup_time', 'booking_time', 'duration', 'client',
                  'transaction_amt', 'ord_id', 'transaction_id','status','duration_unit')
        #depth=1

class DealerDetailSerializer(serializers.ModelSerializer):
    reverseAdd = serializers.CharField(read_only=True)
    dealer_name=serializers.CharField(read_only=True)
    
    class Meta:
        model = DealerDetail
        fields = ('id', 'dealer_name','extra_info', 'thumbnail',
                  'image', 'latitude', 'longitude', 'reverseAdd')
        read_only_fields = ('thumbnail', )
        #depth = 1





