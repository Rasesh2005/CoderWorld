from blog.models import BlogComment, Post
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
# Create your views here.
def blogHome(request):
    allPosts=Post.objects.all()
    context={
        "allPosts":allPosts
    }
    return render(request,'blog/blogHome.html',context=context)

def blogPost(request,slug):
    post=Post.objects.filter(slug=slug).first()
    comments=BlogComment.objects.filter(post=post)
    context={
        "post": post,
        'comments':comments
    }
    return render(request,'blog/blogPost.html',context=context)


def postComment(request):
    if request.method=="POST":
        comment=request.POST['comment']
        user=request.user
        sno=request.POST['sno']
        post=Post.objects.get(sno=sno)
        comment=BlogComment(comment=comment,user=user,post=post)
        comment.save()
        messages.success(request,'Your Comment Has been posted successfully')
    else:
        messages.error(request,'Some Error Occured While Commenting')
    return redirect(f'/blog/{post.slug}/')