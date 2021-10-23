from django.shortcuts import render,redirect,HttpResponseRedirect
from .models import *
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth.models import User,Group
from adminapp.models import *
from django.db.models import Q
from django.core.paginator import Paginator
import math


def auhome(request):
    return render(request,'authorapp/auhome.html')

@login_required(login_url='/')
def home(request):
    popular_books = Book.objects.filter(status='Published').order_by('likes').reverse()[:6]
    latest_books = Book.objects.filter(status='Published')
    print(popular_books)
    context = {'popular_books':popular_books}
    return render(request,'home.html',context)

def book(request,book_id=None):
    book = Book.objects.get(id = book_id)
    user= User.objects.get(username=request.user)
    book_viewers = book.book_viewers.split(' +')
    if not str(request.user) in book_viewers:
        book.book_viewers += str(user.username) + ' +'
        book.book_views += 1
        book.save()
    comments = Comment.objects.filter(book_name=book)
    reply = Comment.objects.filter(book_name=book).exclude(parent=None)
    book.comments = len(comments)
    book.save()
    context = {'book':book,'comments':comments,'reply':reply}
    return render(request,'authorapp/book.html',context)



def like(request,pk):
    book = Book.objects.get(id=pk)
    p_like = Like.objects.filter(user=str(request.user),book_name_id=pk)
    dup = False
    for i in p_like:
        if i.user == str(request.user):
            dup = True
    
    if not dup:
        like = Like(user=str(request.user),book_name_id=pk,like_time=timezone.now())
        like.save()
        up_like = Like.objects.filter(book_name_id=pk)
        book.likes = len(up_like)
        book.save()
    else:
        messages.warning(request, 'You already like this Book')
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) ## return to same page 

def comment(request,pk):
    if request.method == 'POST':
        comment = Comment()
        comment.user = request.user
        book = Book.objects.get(id=pk)
        comment.book_name = book
        comment.book_comment = request.POST['comment']
        
        reply = request.POST.get('reply')

        if reply == None:
            comment.save()
            messages.success(request,'Your Comment Added Sucessfully')
        else:
            comment.reply = True 
            com = Comment.objects.get(id=reply)
            comment.parent = com
            comment.save()
            messages.success(request,'Your Reply Added Sucessfully')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) ## return to same page 

def comment_like(request,pk):
    comment = Comment.objects.get(id=pk)
    likers = comment.like_by.split(', ')
    print(likers)
    if not str(request.user.id) in likers:
        comment.comment_like += 1
        comment.like_by += str(request.user.id) + ', '
        comment.save()
    else:
        messages.warning(request,'You already liked this comment')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) ## return to same page




def addbook(request):
    if request.method == 'POST':
        book = Book()
        book.name = request.POST['name']
        book.author = request.POST['author']
        book.genre = request.POST['genre']
        book.cover = request.FILES['cover']
        book.pdf = request.FILES['pdf']
        book.summary = request.POST['summary']
        book.upload_by = request.user
        
        book.save()

        messages.success(request,'Your Book Added Sucessfully')
        return redirect('home')

    context =  {}
    return render(request,'authorapp/addbook.html')

def update_book(request,book_id=None):
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST,instance=book)
        if form.is_valid():
            form.save()
            messages.success(request,'Your Book Updated Sucessfully')
            return redirect('books')
    else:
        form = BookForm(instance=book)
    context = {'form':form}
    return render(request,'authorapp/update_book.html',context)
    

def addbook_profile(request):
    if request.method == 'POST':
        book = Book()
        book.name = request.POST['name']
        book.author = request.POST['author']
        book.genre = request.POST['genre']
        book.cover = request.FILES.get('cover',None)
        book.pdf = request.FILES.get('pdf',None)
        book.summary = request.POST['summary']
        book.upload_by = request.user
        
        book.save()

        messages.success(request,'Your Book Added Sucessfully')
        return redirect('profile')
    
    context =  {}
    return render(request,'authorapp/addbook_profile.html')


def books(request):
    books = Book.objects.filter(upload_by=request.user)
    context = {'books':books}
    return render(request,'authorapp/books.html',context)


def delete_book_request(request):
    if request.method == 'POST':

        book_id = request.POST['book_id']
        reason = request.POST['reason']
        book = Book.objects.get(id=book_id)
        request_by = request.user
        book_name = book.name
        publisher = book.upload_by
        author = book.author
        
        reader = Reader.objects.get(username=str(request.user))
        ps = reader.position
        group = Group.objects.get(name=ps)
        
        book_id = int(book_id)
        
        del_book_id = DeleteRequest.objects.filter(Q(book_id=book_id) & Q(request_by=request.user))
        
        ids = []
        for i in del_book_id:
            if not i.book_id in ids:
                ids.append(i.book_id)

        if book_id in ids:
            messages.warning(request,'You already send delete request for this book')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) ## return to same page 
    
        
        del_req = DeleteRequest(book_id=book_id,request_by=request_by,book_name=book_name,publisher=publisher,author=author,position=group,reason=reason)

        del_req.save()
        messages.success(request,'Your Delete Request Submitted Sucessfully')

        return redirect('home')

    return render(request,'authorapp/delete_book_request.html')

    


def delete_requested_books(request):
    del_req_books = DeleteRequest.objects.filter(publisher=str(request.user))
    
    books_ids = []

    for i in del_req_books:
        if not i.book_id in books_ids:
            books_ids.append(i.book_id)

        
    del_books = []
    for id in books_ids:
        book = DeleteRequest.objects.filter(book_id=id)[0]
        if not book in del_books:
            del_books.append(book)
    
    books = DeleteRequest.objects.filter(book_id__in=books_ids)
    context = {'books':del_books,'requests':books}
    return render(request,'authorapp/delete_requested_books.html',context)


def change_book_status(request,book_id):
    book = Book.objects.get(id=book_id)
    if book.status == 'Unpublish':
        book.status = 'Published'
    else:
        book.status = 'Unpublish'
    
    book.save()
    messages.success(request,f'Book status changed to {book.status}')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) ## return to same page 


def liked_book(request):
    like_books = Like.objects.filter(user=str(request.user))
    print(like_books)
    name = []
    for i in like_books:
        book = i.book_name
        name.append(book)
    
    books = Book.objects.filter(name__in=name)
    context ={'books':books}
    return render(request,'authorapp/liked_book.html',context)

def delete_book(request,book_id=None):
    book = Book.objects.get(pk=book_id)
    book.delete()
    messages.success(request,'Book Deleted Successfully')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 

def add_to_wishlist(request,book_id=None):
    
    book_id = int(book_id)

    wishlist = Wishlist.objects.filter(Q(user=request.user) & Q(book_id=book_id))
    
    if len(wishlist) > 0:
        messages.warning(request,'This Book Already added to your wishlist')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
    
    else:
        book = Book.objects.get(pk=book_id)
        wish = Wishlist(book_id=book_id,book_name=book,user=request.user,book_author=book.author)
        wish.save()
        messages.success(request,'Book Added to Your ReadList')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    context = {'books':wishlist}
    return render(request,'authorapp/wishlist.html',context)


