from django.contrib import admin
from .models import BlogComment, Post
# Register your models here.
admin.site.register(BlogComment)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    class Media:
        js=('js/tinyInject.js',)