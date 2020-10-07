from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
def blogHome(request):
    return render(request,'blogHome.html')

def blogPost(request,slug):
    return render(request,'blogPost.html')