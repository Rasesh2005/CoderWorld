from . import views
from django.urls import path

urlpatterns = [
    path('', views.blogHome,name='blogHome'),
    path('<str:slug>/', views.blogPost,name='blogPost'),
]