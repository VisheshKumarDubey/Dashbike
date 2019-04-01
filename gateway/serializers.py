from rest_framework import serializers
from .models import *


class TrxnSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrxnDetail
        fields = ('MID', 'ORDER_ID', 'CUST_ID', 'TXN_AMOUNT', 'CHANNEL_ID', 'WEBSITE', 'INDUSTRY_TYPE_ID',  # 'CHECKSUMHASH',
                  'MOBILE_NO', 'EMAIL', 'CALLBACK_URL')  # , 'MODE','CHECKSUM')