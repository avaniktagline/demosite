from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
import json 
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


# Create your models here.
def validate_not_empty(value):
    # print("===call====", value)
    if value == '':
        raise ValidationError('%(value)s is empty!')


class Company(models.Model):
    c_name = models.CharField(max_length=250, null=False, validators=[validate_not_empty])
    address = models.TextField(max_length=250, null=False, validators=[validate_not_empty])
    phone_regex = RegexValidator(
        regex=r'^(91)\d{10}$',
    )
    mobile = models.CharField(validators=[phone_regex, validate_not_empty], max_length=60, null=False)
    email = models.EmailField(max_length=254, null=False, unique=True, validators=[validate_email, validate_not_empty])
    website = models.CharField(max_length=250, null=False, validators=[validate_not_empty])

    def __str__(self):
        return self.c_name

    def save(self):
        super().full_clean()
        super().save()


class User(AbstractUser): 
    id = models.AutoField(primary_key=True)
    is_admin = models.BooleanField(default=False)
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE) 
    name = models.CharField(max_length=250, null=False, validators=[validate_not_empty])
    username = models.CharField(max_length=250, unique=True, null=False, validators=[validate_not_empty])
    email = models.EmailField(max_length=254, null=False, unique=True, validators=[validate_email, validate_not_empty])
    gen = (('male', 'male'), ('female', 'female'), ('other', 'other'))
    gender = models.CharField(max_length=6, choices=gen, null=False, validators=[validate_not_empty])
    hobby = models.CharField(max_length=250, null=False, validators=[validate_not_empty])

    def __str__(self):
        return self.username

    def save(self):
        super().full_clean()
        super().save()

    def hobby_list(self):
        if self.hobby == "":
            return
        strtolist = json.loads(self.hobby.replace("'", '"'))
        listtostr = ", ".join(strtolist)
        return listtostr
    
    