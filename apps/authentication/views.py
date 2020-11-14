from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.

def register(request, *args, **kwargs):
    return HttpResponse('Register Page')