from django.shortcuts import render,redirect
from authorapp.models import *

# Create your views here.
def uhome(request):
    return render(request,'userapp/uhome.html')