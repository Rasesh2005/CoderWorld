from django.http import request
from blog.models import Post
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
import requests
import json
# Create HTML Views
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

        clientKey=request.POST['g-recaptcha-response']
        secretKey='6LfuEtYZAAAAACWA4m9rlRnn8mGQBm-2Erbw2-PG'
        captchaContent={
            "secret": secretKey,
            "response":clientKey
        }
        r=requests.post("https://www.google.com/recaptcha/api/siteverify",data=captchaContent)
        response=json.loads(r.text)
        success=response['success']
        print(success)
        if not success:
            messages.error(request, 'You need to complete the reCaptcha to contact me')
            return redirect("home_app:contact")
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, 'Please Follo wthe Rules of minimum length...')
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

# Authentication API
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
        clientKey=request.POST['g-recaptcha-response']
        secretKey='6LfuEtYZAAAAACWA4m9rlRnn8mGQBm-2Erbw2-PG'
        captchaContent={
            "secret": secretKey,
            "response":clientKey
        }
        r=requests.post("https://www.google.com/recaptcha/api/siteverify",data=captchaContent)
        response=json.loads(r.text)
        success=response['success']
        if not success:
            messages.error(request, 'You need to complete the reCaptcha to contact me')
            return redirect("home_app:home")
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
        user=authenticate(username=username,password=pass1)
        if user:
            login(request,user)
            messages.success(request,"Successfuly logged in")
        else:
            messages.error(request,"Something went wrong when trying to log in automatically")
        return redirect("home_app:home")

    else:
        return HttpResponse("404 - NOT FOUND")
def handleLogin(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        clientKey=request.POST['g-recaptcha-response']
        secretKey='6LfuEtYZAAAAACWA4m9rlRnn8mGQBm-2Erbw2-PG'
        captchaContent={
            "secret": secretKey,
            "response":clientKey
        }
        r=requests.post("https://www.google.com/recaptcha/api/siteverify",data=captchaContent)
        response=json.loads(r.text)
        success=response['success']
        if not success:
            messages.error(request, 'You need to complete the reCaptcha to contact me')
            return redirect('home_app:home')
        elif user:
            login(request,user)
            messages.success(request,"Successfuly logged in")
            return redirect('home_app:home')
        else:
            messages.error(request,"Invalid Credentials.. Please Try Again")
            return redirect('home_app:home')
    else:
        return HttpResponse("404 - NOT FOUND")

@login_required
def handleLogout(request):
    logout(request)
    messages.success(request,"Successfuly logged out")
    return redirect('home_app:home')

@login_required
def myAccount(request):
    if request.method=="POST":
        user=request.user
        username=request.POST.get('userName')
        if request.POST['btn']=='Update':
            email=request.POST.get('userAddress')
            user.username=username
            user.email=email
            user.save()
        else:
            password=request.POST.get('pass')
            pass1=request.POST.get('pass1')
            pass2=request.POST.get('pass2')
          
            matchcheck= check_password(password,user.password)
            if not matchcheck:
                messages.error(request,"The Current Passwords wa incorrect")
            elif pass1!=pass2:
                messages.error(request,"The New Passwords Do Not match")
            else:
                user.set_password(pass1)
                user.save()
                messages.success(request,"Password changed successfully!") 
    return render(request,'profile/account.html',context={'user':request.user})