from django.shortcuts import render
from django.http import HttpResponse
from Reports.models import *
# Create your views here.

def home_index(request):
    return HttpResponse('Reports have been successfully created:')