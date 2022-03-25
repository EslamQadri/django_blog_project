from django.contrib import admin

# Register your models here.
from .models import Post,Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=['title','slug','auther','publish','status']
    list_filter=['status','created','publish']
    search_fields=['title','body']
    prepopuated_fields={'slug': ('title')}
    raw_id_fields=('auther',)
    date_hierarchy='publish'
    ordering=('status','publish') 

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=('name','email','post','created','updated','active')
    list_filter=('active','email','body')
    search_fields=('name','email','post')
    