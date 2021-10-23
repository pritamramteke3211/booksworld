from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id','name','author','category','upload_at']
