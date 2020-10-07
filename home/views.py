from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'home/home.html')
def about(request):
    return HttpResponse("This is About")
def contact(request):
    return HttpResponse("This is Contact")