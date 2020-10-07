from django.urls import path
from . import views
app_name='home_app'
urlpatterns = [
    path('', views.home,name="home"),
    path('about/', views.about,name="about"),
    path('contact/', views.contact,name="contact"),
    path('search/', views.search,name="search"),
]