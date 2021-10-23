from django.contrib import admin
from .models import *


class LikeInline(admin.TabularInline):
    model = Like
    extra = 1

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id','name','author','upload_by','status','likes','comments','upload_at']
    inlines = [LikeInline,CommentInline]

@admin.register(DeleteRequest)
class DeleteRequestAdmin(admin.ModelAdmin):
    list_display = ['id','book_id','book_name','author','request_by','position','publisher']

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['id','book_id','book_name','book_author','user','add_time']


