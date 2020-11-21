from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.views.generic import TemplateView
from django.views import generic
from django.contrib import messages
from .models import *
from django.contrib.auth import *
from django.contrib.auth.hashers import make_password

# Create your views here.
        
class Home(generic.TemplateView):
    template_name = 'index.html'
    model = Company

    def get(self, request):
        user_login = request.session.get("user_login", False)
        if user_login is True:
            u = request.session["user_data"]
            user = User.objects.get(email=u['email'])
            return render(request, self.template_name, {'user': user})
        else:
            return HttpResponseRedirect('/login')
    

# class Signup(generic.TemplateView):
#     template_name = 'registration.html'
#     model = User

#     def get(self, request):
#         user_login = request.session.get("user_login", False)
#         if user_login is True:
#             return HttpResponseRedirect('/')
#         else:
#             return render(request, self.template_name)
    
#     def post(self, request):
#         name = self.request.POST.get('name')
#         username = self.request.POST.get('username')
#         email = self.request.POST.get('email')
#         gender = self.request.POST.get('gender')
#         hobby = self.request.POST.getlist('chk')
#         password = self.request.POST.get('password')
#         try:
#             u = User.objects.create(name = name, username = username, email = email, gender = gender, hobby = hobby,)
#             u.password = make_password(password = password)
#             u.save()
#             return HttpResponseRedirect('/login')
#         except Exception as e:
#             return render(request, self.template_name, {'msg':e})           


class Login(generic.TemplateView):
    template_name = 'login.html'
    model = User

    def get(self, request):
        user_login = request.session.get("user_login", False)
        if user_login is True:
            return HttpResponseRedirect('/')
        else:
            return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = self.request.POST.get('email')
        password = self.request.POST.get('password')
        try:
            u = User.objects.get(email=email)
            message = "Invalid password"
            if u.check_password(password) is True:
                request.session['user_login'] = True
                udata = {'id' : u.id, 'name' : u.name, 'email' : u.email, 'is_admin' : u.is_admin }
                request.session['user_data'] = udata
                return HttpResponseRedirect('/')
            else:
                return render(request, self.template_name, {'msg': message})
        except Exception:
            message = "Invalid email"
            return render(request, self.template_name, {'msg': message})
    

def logout(request):
    if request.session["user_login"]:
        del request.session['user_login']
    return HttpResponseRedirect('/login')
    

class EditUser(generic.TemplateView):
    template_name = 'index.html'
    model = User

    def post(self, request, *args, **kwargs):
        user_id = kwargs['id']
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        hobby = request.POST.getlist('hobby[]')
        try:
            user = User.objects.get(id=user_id)
            user.name = name
            user.username = username
            user.email = email
            user.gender = gender
            user.hobby = hobby
            user.save()
            message = "User details successfully updated"
            return JsonResponse({'success': 'True', 'msg':message})
        except Exception as e:
            return JsonResponse({'success': 'False', 'msg':str(e)})


class ListCompany(generic.TemplateView):
    template_name = 'companylist.html'
    model = Company

    def get_context_data(self, **kwargs):
        context = super(ListCompany, self).get_context_data(**kwargs)
        context['companies'] = Company.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        cname = self.request.POST.get('cname')
        caddress = self.request.POST.get('caddress')
        cmobile = self.request.POST.get('cmobile')
        cemail = self.request.POST.get('cemail')
        cwebsite = self.request.POST.get('cwebsite')
        try:
            Company.objects.create(c_name = cname, address = caddress, mobile = cmobile, email = cemail, website = cwebsite)
            message = "Company added successfully"
            return JsonResponse({'success': 'True', 'msg':message})
        except Exception as e:
            return JsonResponse({'success': 'False', 'msg':str(e)})


class ListEmployee(generic.TemplateView):
    template_name = 'employeelist.html'
    model = User, Company

    def get_context_data(self, **kwargs):
        context = super(ListEmployee, self).get_context_data(**kwargs)
        context['users'] = User.objects.all()
        context['companies'] = Company.objects.all()
        return context
    
    def post(self, request, *args, **kwargs):
        name = self.request.POST.get('name')
        username = self.request.POST.get('username')
        email = self.request.POST.get('email')
        gender = self.request.POST.get('gender')
        hobby = self.request.POST.getlist('hobby[]')
        company = self.request.POST.get('company')
        password = self.request.POST.get('password')
        try:
            u = User.objects.create(name = name, username = username, email = email, gender = gender, hobby = hobby, company_id = company,)
            u.password = make_password(password = password)
            u.save()
            return JsonResponse({'status': 'success', 'msg':message})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'fail', 'msg':str(e)})