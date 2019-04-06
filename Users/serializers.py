from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model, authenticate
from rest_auth.serializers import TokenSerializer, LoginSerializer
from rest_auth.models import TokenModel
from .models import DealerDetail, ClientDetail, CustomUser


class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    number = serializers.CharField(required=True)

    user_type = serializers.ChoiceField(
        choices=(
            ('Client', 'Client'),
            ('Dealer', 'Dealer'),

        ),
        style={'base_template': 'radio.html'},
        required=True, write_only=True)

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()
        print(self.validated_data.get('number', ''))
        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'username': self.validated_data.get('username', ''),
            'user_type': self.validated_data.get('user_type', ''),
            'number': self.validated_data.get('number', ''),
        }


class DealerProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = DealerDetail
        fields = '__all__'
        read_only_fields = ('thumbnail', )
        #depth=1


class ClientProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ClientDetail
        fields = '__all__'
        read_only_fields = ('thumbnail', )
        # depth=1


class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("user_type",)


class TokenSerializer(serializers.ModelSerializer):
    """
    Serializer for Token model.
    """
    user = CheckSerializer(
        many=False, read_only=True)  # this is add by myself.

    class Meta:
        model = TokenModel
        fields = ('key', 'user')
