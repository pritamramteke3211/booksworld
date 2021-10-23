from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id','name','author','category','likes','comments','upload_at']
    
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id','book_name','user_name','like_time']

@admin.register(Comment)
class Comment(admin.ModelAdmin):
    list_display = ['id','book_name','user','comment_like','comment_time']
