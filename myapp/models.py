from django.db import models

# Create your models here.

class User(models.Model):  
    name = models.CharField(max_length=250)  
    email  = models.CharField(max_length=50)
    gender = models.CharField(max_length=250, default="")
    hobby = models.CharField(max_length=250, default="")
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    