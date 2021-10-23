from os import truncate
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import PROTECT
from django.utils import timezone

GENRE = (('Fiction','Fiction'),
('Non-Fiction','Non-Fiction'))
Position = (('Reader','Reader'),('Publisher','Publisher'),('Author','Author'),('Admin','Admin'))
STATUS = (('Published','Published'),('Unpublish','Unpublish'))

# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=100,blank=True)
    cover = models.ImageField(upload_to='images/Book_cover/', null=True,blank=True, default='images/Book_cover/default_book_cover_3.png')
    pdf = models.FileField(upload_to='documents/book_pdf/', null=True,blank=True)
    summary = models.TextField(blank=True)
    buy_link = models.URLField(blank=True, null=True)
    upload_at = models.DateTimeField(default=timezone.now, blank=True)
    upload_by = models.ForeignKey(User,on_delete=PROTECT,null=True)
    status = models.CharField(choices=STATUS,default='Unpublish',max_length=20)
    book_viewers = models.CharField(default='',max_length=500,blank=True)
    book_views = models.IntegerField(default=0)
    
    
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)

    def __str__(self):
        return str(self.name)
    

class Like(models.Model):
    book_name = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.CharField(default='',blank=True,max_length=100)
    like_time = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return str(self.book_name)

      

class Comment(models.Model):
    user = models.CharField(max_length=200 ,blank=True)
    book_name = models.ForeignKey(Book, on_delete=models.CASCADE)
    book_comment = models.CharField(max_length=1000,blank=True)
    comment_like = models.IntegerField(default=0)
    like_by = models.CharField(max_length=1000,default='',blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True,blank=True) ## parent is field of self.model 
  
    reply = models.BooleanField(default=False,null=True)
    comment_time = models.DateTimeField(default=timezone.now)

class DeleteRequest(models.Model):
    request_by = models.ForeignKey(User,on_delete=models.CASCADE)
    book_id = models.IntegerField()
    book_name = models.CharField(max_length=100,default='')
    position = models.CharField(max_length=10,choices=Position,default='Reader')
    publisher = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    reason = models.TextField(default='')

    def __str__(self):
        return self.book_name

class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    book_id = models.IntegerField()
    book_name = models.ForeignKey(Book, on_delete=models.CASCADE)
    book_author = models.CharField(max_length=100,default='')
    add_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.book_name)


