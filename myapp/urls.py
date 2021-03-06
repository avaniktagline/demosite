"""demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from . import views 

urlpatterns = [
    path('', views.Home.as_view(), name='index'),
    # url(r'^signup/$', views.Signup.as_view(), name='signup'),
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    path('edituser/<int:id>', views.EditUser.as_view(), name='edituser'),
    path('listcompany', views.ListCompany.as_view(), name='listcompany'),
    path('editcompany', views.EditCompany.as_view(), name='editcompany'),
    path('deletecompany', views.DeleteCompany.as_view(), name='deletecompany'),
    path('listemployee', views.ListEmployee.as_view(), name='listemployee'),
    path('editemployee', views.EditEmployee.as_view(), name='editemployee'),
    path('deleteemployee', views.DeleteEmployee.as_view(), name='deleteemployee'),
]
