from django.shortcuts import render

# Create your views here.
def adhome(request):
    return render(request,'adminapp/adhome.html')
