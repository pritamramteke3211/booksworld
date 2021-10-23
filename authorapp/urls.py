from django.urls import path
from . import views

urlpatterns = [
    path('',views.auhome,name='auhome'),
    path('home/', views.home, name='home'),
    path('book/<int:book_id>', views.book, name='book'),
    path('like/<int:pk>', views.like, name='liked'),
    path('addbook/', views.addbook, name='addbook'),
    path('update_book/<int:book_id>', views.update_book, name='update_book'),
    path('addbook_profile/', views.addbook_profile, name='addbook_profile'),
    path('books/', views.books, name='books'),
    path('delete_book_request/', views.delete_book_request, name='delete_book_request'),
    path('delete_requested_books/', views.delete_requested_books, name='delete_requested_books'),
    path('change_book_status/<int:book_id>', views.change_book_status, name='change_book_status'),
    path('liked_book', views.liked_book, name='liked_book'),
    path('delete_book/<int:book_id>', views.delete_book, name='delete_book'),
    path('add_to_wishlist/<int:book_id>', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist', views.wishlist, name='wishlist'),
    path('comment/<int:pk>', views.comment, name='comment'),
    path('comment_like/<int:pk>', views.comment_like, name='comment_like'),

]