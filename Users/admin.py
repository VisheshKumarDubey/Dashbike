from django.contrib import admin
from .models import CustomUser,ClientDetail,DealerDetail
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(ClientDetail)
admin.site.register(DealerDetail)