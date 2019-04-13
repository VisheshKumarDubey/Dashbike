"""Dashbike URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf.urls import url
from django.contrib import admin
import Users.urls
from django.conf import settings
from django.conf.urls.static import static
import api.urls
import test1.urls
import pushnotifications.urls



urlpatterns = [
    url(r'^api/v1/', include(Users.urls)),
    path('api/v1/', include(api.urls)),
    path('api/v1/', include(pushnotifications.urls)),
    path('', include(test1.urls)),
    path('admin/', admin.site.urls),
   # path('api/v1/', include(gateway.urls))
]
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
