from django.contrib import admin
from .models import BlogComment, Post
# Register your models here.
admin.site.register((BlogComment,Post))