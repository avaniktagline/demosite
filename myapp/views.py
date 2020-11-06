from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views import generic
from django.contrib import messages
from .models import *
from django.contrib.auth import *
from django.contrib.auth.hashers import make_password
from myapp.decorator import user_login_required
from django.utils.decorators import method_decorator
import logging

# Create your views here.
        
@method_decorator(user_login_required, name='dispatch')
class Home(generic.TemplateView):
    template_name = 'index.html'


@method_decorator(user_login_required, name='dispatch')    
class Signup(generic.TemplateView):
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
            return HttpResponseRedirect('/login')
        except Exception as e:
            return render(request, self.template_name, {'msg':e})           


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
                request.session['user_login'] = True
                request.session['user_data'] = {'name' : u.name, 'email' : u.email}
                return redirect('/')
            else:
                return render(request, self.template_name, {'msg': message})
        except Exception:
            message = "Invalid email"
            return render(request, self.template_name, {'msg': message})
    

def logout(request):
    if request.session.get('user_login', True):
        # print("===before===", request.session['user_login'])
        del request.session['user_login']
        request.session.modified = True
        # print("===after===", request.session['user_login'])
    return HttpResponseRedirect('/login')
