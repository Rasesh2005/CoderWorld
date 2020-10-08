from blog.models import Post
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
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


def handleSignup(request):
    if request.method=="POST":
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        user=User.objects.create_user(username,email,pass1,first_name=fname,last_name=lname)
        user.save()
        if pass1!=pass2:
            messages.error(request,'Passwords do not match')
            return redirect("home_app:home")
        if len(username)>20:
            messages.error(request,'Username Length Should be less than 20 characters')
            return redirect("home_app:home")
        if not username.isalnum():
            messages.error(request,'Username Must be alphanumeric')
            return redirect("home_app:home")
        messages.success(request,'Your Account Has Been Successfuly created')
        return redirect("home_app:home")
    else:
        return HttpResponse("404 - NOT FOUND")

def handleLogin(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user:
            login(request,user)
            messages.success(request,"Successfuly logged in")
            return redirect('home_app:home')
        else:
            messages.error(request,"Invalid Credentials.. Please Try Again")
            return redirect('home_app:home')
    else:
        return HttpResponse("404 - NOT FOUND")

def handleLogout(request):
    logout(request)
    messages.success(request,"Successfuly logged out")
    return redirect('home_app:home')