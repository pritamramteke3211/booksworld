
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.views import *
from authorapp.models import *
from adminapp.models import *
from django.contrib.auth.models import User,Group
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.core.paginator import Paginator
from django.db.models import Q






def get_feedback(request):
    if request.method == "POST":
        feedback = request.POST["feedback"]
        feed = Feedback(user=request.user,feedback=feedback)
        feed.save()
        messages.success(request,'Thanks For Your Feedback')
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def prac(request):
    
    context = {}
    return render(request,'prac.html',context)

def signup(request):
    if request.method == 'POST':
        us =request.POST['username']
        em = request.POST['email']
        ps = request.POST['position']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        

        if pass1 != pass2 :
            messages.error(request,'Password Fields Not Matched!')
            return redirect('signup')
        
        if not us.isalnum():
            messages.error(request,'username contains only letters and numbers!')
            return redirect('signup')
        
        if not us.islower():
            messages.error(request,'username must in lowercase!')
            return redirect('signup')

        if len(us) < 4:
            messages.error(request,'username must 4 or more characters long!')
            return redirect('signup')

        if len(pass1) < 7:
            messages.error(request,'password must 7 or more characters long!')
            return redirect('signup')
        
        reader = Reader(username=us,email=em,password=pass1,position=ps)
        
        user = User.objects.create_user(username=us,email=em,password=pass1)
        group = Group.objects.get(name=ps)
        user.groups.add(group)
        reader.save()
        user.save()
        
        messages.success(request,f'{ps} added successfully')
        return redirect('login')

   
    context = {}
    return render(request,'signup.html',context)
    

@method_decorator(login_required, name='dispatch')
class UserProfile(View):
    template_name = 'profile.html'
    def get(self, request):
        books = Book.objects.filter(upload_by=request.user)
        published_books = Book.objects.filter(Q(status='Published' ) & Q(upload_by=request.user))
        unpublished_books = Book.objects.filter(Q(status='Unpublish') & Q(upload_by=request.user))
        del_req = DeleteRequest.objects.filter(publisher=str(request.user))
        wishlist = Wishlist.objects.filter(user = request.user)
        like_boooks = Like.objects.filter(user=str(request.user))
        context = {'books':books,'del_req':del_req,'wishlist':wishlist,'like_boooks':like_boooks,'published_books':published_books,'unpublished_books':unpublished_books}
        return render(request,self.template_name,context)

    
def user_login(request):
    errors = []
    if request.method == 'POST':
        un = request.POST['username']
        pw = request.POST['password']

        if len(un) == 0 :
            errors.append('username field is empty')

        if len(pw) == 0 :
            errors.append('password field is empty')

        
        user = authenticate(username = un, password=pw)
        if user is not None:
            login(request,user)
            # messages.success(request,f'Welcome {request.user}!')
            return redirect('home')

        else:
            errors.append('Invalid credentials!')
    
    print(errors)
    return render(request,'login.html',{'errors':errors})

    
class MyLogoutView(LogoutView):
    template_name='logout.html'
    
class MyPasswordChangeView(PasswordChangeView):
    template_name='changepass.html'

    
class MyPasswordChangeDoneView(PasswordChangeDoneView):
    template_name='password_change_done.html'
   
class MyPasswordResetView(PasswordResetView):
    template_name='password_reset.html'
    
class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name='password_reset_done.html'
    
class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name='password_reset_confirm.html'
    
class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name='password_reset_complete.html'

def book_search(request):
    equery = request.GET.get('search')
    query = equery
    print(query)
    if query:
        query = query.strip()
        query = query.lower()

    # book = Book.objects.get(pk=1)
   
    books = Book.objects.values('name','author','id')
    print(books)
    
   
    book_name_list  = [i['name'] for i in books]
    book_author_list  = [i['author'] for i in books]
    book_id_list  = [i['id'] for i in books]

    print(book_name_list)
    print(book_author_list)
    print(book_id_list)

 
 
    book_ids = []
    for i in book_name_list:
        if i.lower() == query:
            item = Book.objects.get(name = i)
            book_ids.append(item.id)
        else:
            for  j in i.split():
                if j.lower() == query:
                    item = Book.objects.get(name = i)
                    book_ids.append(item.id)

    for i in book_author_list:
        if i.lower() == query:
            item = Book.objects.get(author = i)
            book_ids.append(item.id)
        else:
            for  j in i.split():
                if j.lower() == query:
                    item = Book.objects.get(author = i)
                    book_ids.append(item.id)

    for i in book_id_list:
        if str(i) == query:
            item = Book.objects.get(id=i)
            book_ids.append(item.id)

    print(book_ids)


    book_ids = set(book_ids)
    book_ids = list(book_ids)
    books = Book.objects.filter(Q(pk__in=book_ids) &  Q(status='Published')).order_by('id')

    paginator = Paginator(books, 4, orphans=2)  ## Don't forget to import - from django.core.paginator import Paginator
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'books':books, 'query':equery,'page_obj':page_obj}
    return render(request,'search.html', context)
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
