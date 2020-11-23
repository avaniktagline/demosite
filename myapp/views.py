from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.core import serializers
import json
from django.views.generic import TemplateView
from django.views import generic
from django.views.generic.base import View
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


class EditCompany(generic.TemplateView):
    template_name = 'companylist.html'
    model = Company

    def get(self, request, *args, **kwargs):
        company_id = self.request.GET.get('company_id')
        cdata = Company.objects.filter(id=company_id)
        company_list = serializers.serialize('json', cdata)
        # print("==========json data==", json.loads(company_list)[0]['fields'])
        return JsonResponse(json.loads(company_list)[0]['fields'])

    def post(self, request, *args, **kwargs):
        company_id = request.POST.get('company_id')
        cname = request.POST.get('cname')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        website = request.POST.get('website')        
        # print(request.POST)
        try:
            company = Company.objects.get(id=company_id)
            company.c_name = cname
            company.email = email
            company.mobile = mobile
            company.address = address
            company.website = website
            company.save()
            message = "Company details successfully updated"
            return JsonResponse({'success': 'True', 'msg':message})
        except Exception as e:
            return JsonResponse({'success': 'False', 'msg':str(e)})


class DeleteCompany(View):
    def get(self, request, *args, **kwargs):
        company_id = self.request.GET.get('company_id')
        Company.objects.filter(id=company_id).delete()
        data = {
            'deleted': True
        }
        return JsonResponse({'success': 'True'})


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
            message = "Employee added successfully"
            return JsonResponse({'success': 'True', 'msg':message})
        except Exception as e:
            return JsonResponse({'success': 'False', 'msg':str(e)})


class EditEmployee(generic.TemplateView):
    template_name = 'employeelist.html'
    model = User

    def get(self, request, *args, **kwargs):
        user_id = self.request.GET.get('user_id')
        udata = User.objects.filter(id=user_id)
        user_list = serializers.serialize('json', udata)
        # print("==========json data==", json.loads(user_list)[0]['fields'])
        return JsonResponse(json.loads(user_list)[0]['fields'])

    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        hobby = request.POST.getlist('hobby[]')
        company = request.POST.get('website')        
        print(request.POST)
        try:
            employee = User.objects.get(id=user_id)
            employee.name = name
            employee.username = username
            employee.email = email
            employee.gender = gender
            employee.hobby = hobby
            employee.company = company
            employee.save()
            message = "Employee details successfully updated"
            return JsonResponse({'success': 'True', 'msg':message})
        except Exception as e:
            return JsonResponse({'success': 'False', 'msg':str(e)})


class DeleteEmployee(View):
    def get(self, request, *args, **kwargs):
        user_id = self.request.GET.get('user_id')
        User.objects.filter(id=user_id).delete()
        data = {
            'deleted': True
        }
        return JsonResponse({'success': 'True'})