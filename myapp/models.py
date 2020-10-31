from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):  
    name = models.CharField(max_length=250)  
    email  = models.EmailField(max_length=50)
    gen = (('male', 'male'), ('female', 'female'), ('other', 'other'))
    gender = models.CharField(max_length=6, choices=gen)
    hobby = models.CharField(max_length=250, default="")

    def __str__(self):
        return self.name

    
    