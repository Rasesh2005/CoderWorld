from . import views
from django.urls import path
app_name='blog_app'
urlpatterns = [
    path('', views.blogHome,name='blogHome'),
    path('<str:slug>/', views.blogPost,name='blogPost'),
]