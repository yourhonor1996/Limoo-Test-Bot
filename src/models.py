from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(models.Model):
    # TODO correct these lengths based on the limitations
    user_id = models.CharField(max_length= 100, unique= True)
    gitlab_token = models.CharField(max_length= 100, null= True, blank= True)
    
class WorkSpace(models.Model):
    workspace_id = models.CharField(max_length= 100)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    

class Conversation(models.Model):
    conversation_id = models.CharField(max_length= 100)
    workspace = models.ForeignKey(WorkSpace, on_delete= models.CASCADE)