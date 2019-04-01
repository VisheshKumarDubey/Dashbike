# users/urls.py
from django.conf.urls import url, include
from django.urls import path
from allauth.account.views import ConfirmEmailView
from . import views
from rest_framework import routers
router = routers.DefaultRouter()
router.register('profile/client', views.ClientViewSet, 'images')
router.register('profile/dealer', views.DealerViewSet, 'images')

urlpatterns = [
    # Override urls
    url(r'^auth/registration/account-email-verification-sent/', views.null_view, name='account_email_verification_sent'),
    url(r'^auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(), name='account_confirm_email'),
    url(r'^auth/registration/complete/$', views.complete_view, name='account_confirm_complete'),
    url(r'^auth/password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.null_view, name='password_reset_confirm'),
    # Default urls
    url(r'auth/', include('rest_auth.urls')),
    url(r'^auth/registration/', include('rest_auth.registration.urls')),
    #url(r'^check/(?P<consultant_id>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', views.check_user),
    #url(r'^profile/',views.UserProfile),
    url(r'^', include(router.urls)),
]