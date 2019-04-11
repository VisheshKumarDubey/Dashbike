from django.urls import path
from django.conf.urls import url
from api import views
from django.conf import settings
from rest_framework.urlpatterns import format_suffix_patterns

if settings.NEARBY_SHOPS:
    urlpatterns = [
    path('booking/', views.BookingList.as_view()),
    path('booking/<int:pk>/', views.BookingDetail.as_view()),
    path('bike/', views.BikeList.as_view()),
    path('bike/<int:pk>/', views.BikeDetail.as_view()),
    url(r'^dealer/(?P<lat>-?\d+.?\d+)/(?P<lon>-?\d+.?\d+)/', views.DealerList.as_view()),
    path('dealer/<int:id>/', views.BikeModelList.as_view()),
    path('dealer/<int:id>/<int:pk>/', views.BikeModelDetail.as_view()),
        ]
else:
    urlpatterns = [
    path('booking/', views.BookingList.as_view()),
    path('booking/<int:pk>/', views.BookingDetail.as_view()),
    path('bike/', views.BikeList.as_view()),
    path('bike/<int:pk>/', views.BikeDetail.as_view()),
    path('dealer/', views.DealerList.as_view()),
    path('dealer/<int:id>/', views.BikeModelList.as_view()),
    path('dealer/<int:id>/<int:pk>', views.BikeModelDetail.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns)
