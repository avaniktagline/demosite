from django.contrib import admin
from .models import *
# Register your models here.

# class UserAdmin(admin.ModelAdmin):
#     list_display = ('name', 'email', 'gender', 'hobby')

admin.site.register(User)
# admin.site.site_header = 'Myapp Admin Panel'
