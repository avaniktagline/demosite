from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Create your models here.

class Company(models.Model):
    c_name = models.CharField(max_length=250, null=False)
    address = models.TextField(max_length=250, null=False)
    phone_regex = RegexValidator(
        regex=r'^(91)\d{10}$',
    )
    mobile = models.CharField(validators=[phone_regex], max_length=60, null=False)
    email = models.EmailField(max_length=250, unique=True, null=False)
    website = models.CharField(max_length=250,  null=False)

    def __str__(self):
        return self.c_name


class User(AbstractUser): 
    id = models.AutoField(primary_key=True)
    is_admin = models.BooleanField(default=False)
    company = models.ForeignKey(Company, blank=True, null=True, on_delete=models.CASCADE) 
    name = models.CharField(max_length=250)
    username = models.CharField(max_length=250, unique=True)
    email  = models.EmailField(max_length=250, unique=True)
    gen = (('male', 'male'), ('female', 'female'), ('other', 'other'))
    gender = models.CharField(max_length=6, choices=gen)
    hobby = models.CharField(max_length=250, blank=True, null=True,)

    def __str__(self):
        return self.username

    def include_hobby(self, hobby):
        listToStr = ','.join([str(hobby) for hobby in self.hobby])
        print(listToStr)
        return listToStr
    
    