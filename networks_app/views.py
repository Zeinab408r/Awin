from urllib import request
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response    
from .tasks import update_and_add_products  
# Create your views here.



def UpdateProduct(request):
       update_and_add_products()
       return HttpResponse("products has updated")
