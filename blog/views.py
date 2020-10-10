from blog.models import BlogComment, Post
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from .templatetags import extras
# Create your views here.
def blogHome(request):
    allPosts=Post.objects.all()
    context={
        "allPosts":allPosts
    }
    return render(request,'blog/blogHome.html',context=context)

def blogPost(request,slug):
    post=Post.objects.filter(slug=slug).first()
    post.views+=1
    post.save()
    comments=reversed(BlogComment.objects.filter(post=post,parent=None))
    replies=reversed(BlogComment.objects.filter(post=post).exclude(parent=None))
    repDict={}
    for reply in replies:
        if reply.parent.sno not in repDict.keys():
            repDict[reply.parent.sno]=[reply]

        else:
            repDict[reply.parent.sno].append(reply)

    context={
        'post': post,
        'comments':comments,
        'replyDict':repDict,
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