from django.db import models
from django.contrib.auth.models import Group,User
from django.utils.timezone import now

Position = (('Reader','Reader'),('Publisher','Publisher'),('Author','Author'),('Admin','Admin'))

# Create your models here.
class Reader(models.Model):
    username = models.CharField(max_length=100)
    
    position = models.CharField(max_length=10,choices=Position,default='Reader')
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username
        

class Feedback(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    feedback = models.TextField()
    timestamp = models.DateTimeField(default = now)

    def __str__(self):
        return str(self.user)





