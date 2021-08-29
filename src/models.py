from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    chat_id = models.CharField(max_length=50)
    
class Message(models.Model):
    message_id = models.CharField(max_length=50)
    date_created = models.DateTimeField()
    is_active = models.BooleanField()
    user = models.ForeignKey(User, on_delete= models.CASCADE)