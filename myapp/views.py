from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views import generic
from django.contrib import messages
from .models import *
from django.contrib.auth import *
from django.contrib.auth.hashers import make_password

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
        try:
            u = User.objects.create(name = name, username = username, email = email, gender = gender, hobby = hobby,)
            u.password = make_password(password = password)
            u.save()
            message = "Registration successfully"
            return render(request, 'login.html', {'success': True, 'msg': message})
        except Exception as e:
            return render(request, self.template_name, {'success': False, 'msg':e})           


class Login(generic.TemplateView):
    template_name = 'login.html'
    model = User

    def post(self, request):
        email = self.request.POST.get('email')
        password = self.request.POST.get('password')
        try:
            u = User.objects.get(email=email)
            message = "Invalid password"
            if u.check_password(password) is True:
                return render(request, 'index.html')
            else:
                return render(request, self.template_name, {'msg': message})
        except Exception:
            message = "Invalid email"
            return render(request, self.template_name, {'msg': message})
    
