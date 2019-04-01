from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from gateway.models import TrxnDetail
from gateway.serializers import TrxnSerializer
from gateway.Checksum import generate_checksum
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

#@login_required
@api_view(['GET', 'POST'])
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = TrxnDetail.objects.all()
        serializer = TrxnSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TrxnSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(settings.PAYTM_MERCHANT_KEY)
            sdata = serializer.data
            mid, order_id, cust_id, txn_amount, channel_id, website, industry_type_id, mobile_no, email, callback = sdata.get('MID'), sdata.get('ORDER_ID'), sdata.get('CUST_ID'), sdata.get(
                'TXN_AMOUNT'), sdata.get('CHANNEL_ID'), sdata.get('WEBSITE'), sdata.get('INDUSTRY_TYPE_ID'), sdata.get('MOBILE_NO'), sdata.get('EMAIL'), sdata.get('CALLBACK_URL')
            param_dict = dict()
            param_dict['MID'] = mid
            param_dict['ORDER_ID'] = order_id
            param_dict['CUST_ID'] = cust_id
            param_dict['TXN_AMOUNT'] = txn_amount
            param_dict['CHANNEL_ID'] = channel_id
            param_dict['WEBSITE'] = website
            param_dict['INDUSTRY_TYPE_ID'] = industry_type_id
           # param_dict['MOBILE_NO'] = mobile_no
           # param_dict['EMAIL'] = email
            param_dict['CALLBACK_URL'] = callback
            # param_dict['']=
            value_dict = dict()
            value_dict['checksum'] = generate_checksum(
                param_dict, settings.PAYTM_MERCHANT_KEY)
            print(generate_checksum(param_dict, settings.PAYTM_MERCHANT_KEY))
            # , status=status.HTTP_201_CREATED)
            return JsonResponse(value_dict)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
