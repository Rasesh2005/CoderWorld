from blog.models import Post
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
def blogHome(request):
    allPosts=Post.objects.all()
    context={
        "allPosts":allPosts
    }
    return render(request,'blog/blogHome.html',context=context)

def blogPost(request,slug):
    post=Post.objects.filter(slug=slug).first()
    context={
        "post": post
    }
    return render(request,'blog/blogPost.html',context=context)