from django.urls import path
from gateway import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('paytm/', views.snippet_list),
]


urlpatterns = format_suffix_patterns(urlpatterns)
