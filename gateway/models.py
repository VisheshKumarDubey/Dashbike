from django.db import models

# Create your models here.


class TrxnDetail(models.Model):
    MID = models.CharField(max_length=20)
    ORDER_ID = models.CharField(max_length=50)
    CUST_ID = models.CharField(max_length=64)
    TXN_AMOUNT = models.CharField(max_length=10)
    CHANNEL_ID = models.CharField(max_length=3)
    WEBSITE = models.CharField(max_length=30)
    INDUSTRY_TYPE_ID = models.CharField(max_length=20)
    # CHECKSUMHASH=models.CharField(max_length=108)
    CALLBACK_URL = models.CharField(max_length=108, null=True)
    MOBILE_NO = models.CharField(max_length=15)
    EMAIL = models.CharField(max_length=50)

    def __str__(self):
        return self.ORDER_ID
