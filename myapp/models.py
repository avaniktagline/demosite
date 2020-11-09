from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=250, null=False)
    address = models.TextField(max_length=250, null=False)
    mobile = models.IntegerField(null=False)
    email = models.EmailField(max_length=250, unique=True, null=False)
    website = models.CharField(max_length=250,  null=False)

    def __str__(self):
        return self.name


class User(AbstractUser): 
    is_admin = models.BooleanField(default=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE) 
    name = models.CharField(max_length=250)
    username = models.CharField(max_length=250, unique=True)
    email  = models.EmailField(max_length=250, unique=True)
    gen = (('male', 'male'), ('female', 'female'), ('other', 'other'))
    gender = models.CharField(max_length=6, choices=gen)
    hobby = models.CharField(max_length=250, default="")

    def __str__(self):
        return self.name

    
    