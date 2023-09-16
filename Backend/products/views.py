from django.shortcuts import render

from django.http import JsonResponse
# Create your views here.
from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
import json
from django.core import serializers

from .mixins import UserQuerySetMixin


class ProductViewSet(
    UserQuerySetMixin,
    viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    lookup_field="pk"

    def perform_create(self, serializer):
        title=serializer.validated_data.get('title')
        content=serializer.validated_data.get('content')
        if content is None:
            content=title
        serializer.save(user=self.request.user,content=content) 

    def get_queryset(self,*args,**kwargs):
        
        qs=super().get_queryset(*args,**kwargs)       

        request=self.request
        user=request.user
        if not user.is_authenticated:
            return Product.objects.none()
        return qs.filter(user=request.user)
    
