from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views import generic
from django.contrib import messages
from .models import *
from django.contrib.auth import *

# Create your views here.

def home_page(request):
    return render(request, 'index.html')

    
class Register(generic.TemplateView):
    template_name = 'registration.html'
    model = User
    
    def post(self, request):
        name = self.request.POST.get('name')
        username = self.request.POST.get('username')
        email = self.request.POST.get('email')
        gender = self.request.POST.get('gender')
        hobby = self.request.POST.getlist('chk')
        password = self.request.POST.get('password')

        user = User.objects.create(name = name, username = username, email = email, gender = gender, hobby = hobby, password = password)
        if user is not None:
            return redirect('login')
        else:
            messages.error(request, 'Not Registration')            


class Login(generic.TemplateView):
    template_name = 'login.html'
    model = User

    def post(self, request):
        email = self.request.POST.get('email')
        password = self.request.POST.get('password')

        user = User.objects.filter(email = email, password = password)
        if user is not None:
            return redirect('index')
        else:
            messages.error(request, 'Invalid Email or Password')