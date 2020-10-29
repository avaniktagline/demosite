from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class RegistrationTemplate(TemplateView):
    template_name = 'registration.html'


