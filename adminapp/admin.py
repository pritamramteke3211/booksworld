from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    list_display=['id','username','position']

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display=['id','user','timestamp']

