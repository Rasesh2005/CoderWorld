from blog.models import Post
from django.http import HttpResponse
from django.shortcuts import render
from .models import Contact
from django.contrib import messages
# Create your views here.
def home(request):
    return render(request,'home/home.html')
def about(request):
    return render(request,'home/about.html')
def contact(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content=request.POST['content']
        contact=Contact(name=name,email=email,phone=phone,content=content)
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, 'Something Went Wrong, Plz Try Submitting Form Again..')
        else:
            try:
                contact.save()
                messages.success(request, 'Contact Form Successfully Submitted.')
            except:
                messages.error(request, 'Something Went Wrong, Plz Try Submitting Form Again..')
    return render(request,'home/contact.html')

def search(request):
    # allPosts=Post.objects.all()
    query=request.GET['query']
    allPostsTitle=Post.objects.filter(title__icontains=query)
    allPostsContent=Post.objects.filter(content__icontains=query)
    allPostsAuthor=Post.objects.filter(author__icontains=query)
    allPosts=allPostsTitle.union(allPostsContent,allPostsAuthor)
    if len(query)>80:
        allPosts=Post.objects.none()
    params={
        "allPosts":allPosts,
        "SearchTerm": query
    }
    return render(request,"home/search.html",context=params)