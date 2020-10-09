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
    comments=reversed(BlogComment.objects.filter(post=post,parent=None))
    replies=reversed(BlogComment.objects.filter(post=post).exclude(parent=None))
    context={
        "post": post,
        'comments':comments
    }
    return render(request,'blog/blogPost.html',context=context)


def postComment(request):
    if request.method=="POST":
        comment=request.POST['comment']
        user=request.user
        sno=request.POST['postSno']
        post=Post.objects.get(sno=sno)
        parentSno=request.POST['parentSno']
        if parentSno=="":
            comment=BlogComment(comment=comment,user=user,post=post)
            comment.save()
            messages.success(request,'Your Comment Has been posted successfully')
        else:
            parent=BlogComment.objects.get(sno=parentSno)
            comment=BlogComment(comment=comment,user=user,post=post,parent=parent)
            comment.save()
            messages.success(request,'Your Reply Has been posted successfully')
        return redirect(f'/blog/{post.slug}/')
    return HttpResponse("Error 404 - Something Went Wrong")