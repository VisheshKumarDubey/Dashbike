from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets, filters
from . models import *
from .serializers import *
from django.contrib.auth.decorators import login_required
from api.permissions import IsOwnerOrReadOnly, IsAdminUserOrReadOnly
from django.shortcuts import redirect,Http404
from rest_framework.exceptions import APIException


@api_view()
def null_view(request):
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view()
def complete_view(request):
    return Response("Email account is activated")


class DealerViewSet(viewsets.ModelViewSet):
    queryset = DealerDetail.objects.all()
    serializer_class = DealerProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self, *args, **kwargs):
        if self.request.user.user_type == 'Dealer':
            return DealerDetail.objects.filter(type=self.request.user)
        else:
            try:
                obj = DealerDetail.objects.filter(type=self.request.user)
            except DealerDetail.DoesNotExist:
                raise Http404("No MyModel matches the given query.")
            return redirect('/api/v1/profile/dealer/')


class ClientViewSet(viewsets.ModelViewSet):
    #queryset = ClientDetail.objects.all()
    serializer_class = ClientProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self, *args, **kwargs):
        if self.request.user.user_type == 'Client':
            return ClientDetail.objects.filter(type=self.request.user)
        else:
            try:
                obj = ClientDetail.objects.filter(type=self.request.user)
            except ClientDetail.DoesNotExist:
                raise Http404("No MyModel matches the given query.")
            return redirect('/api/v1/profile/dealer/')


@login_required
@api_view(['GET', 'PUT', ])
def UserProfile(request):
    if request.user.user_type == 'Dealer':
        try:
            snippet = DealerDetail.objects.get(type=request.user)
        except DealerDetail.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        try:
            snippet = ClientDetail.objects.get(type=request.user)
        except ClientDetail.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        if request.user.user_type == 'Dealer':
            serializer = DealerProfileSerializer(snippet)
            return Response(serializer.data)
        else:
            serializer = ClientProfileSerializer(snippet)
            return Response(serializer.data)
    if request.method == 'PUT':
        if request.user.user_type == 'Dealer':
            serializer = DealerProfileSerializer(snippet, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = ClientProfileSerializer(snippet, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
