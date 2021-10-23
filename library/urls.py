
from django.contrib import admin
from django.urls import path,include
from . import views
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('prac',views.prac, name='prac'),
    path('signup/',views.signup, name='signup'),
    # path('userapp',include('userapp.urls')),
    path('authorapp/',include('authorapp.urls')),
    path('adminapp/',include('adminapp.urls')),
    # path('', views.HomePage.as_view(), name='home'),

    path('feedback', views.get_feedback, name='get_feedback'),

    # path('home/', views.home, name='home'),
    path('profile/', views.UserProfile.as_view(), name="profile"), ## classed view

    path('', views.user_login, name="login"), ## classed view
    
    path('logout/', views.MyLogoutView.as_view(), name='logout'), ## now url_path = /logout/ not accounts/logout/
    path('changepass/', views.MyPasswordChangeView.as_view(), name='changepass'), 
    path('password_change_done/', views.MyPasswordChangeDoneView.as_view(), name='password_change_done'),
   
    path('password_reset/', views.MyPasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/', views.MyPasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.MyPasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/', views.MyPasswordResetCompleteView.as_view(),name='password_reset_complete'),

    path('book_search/',views.book_search,name='book_search')

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)