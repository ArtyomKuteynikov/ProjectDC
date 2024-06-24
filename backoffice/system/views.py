# тут должны быть все view функции связанные с регистрацией и аутентификацией

from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView
from .models import Customer
from .forms import CustomerForm
from django.urls import reverse_lazy


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'system/index.html')


class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'system/registration.html'
    success_url = reverse_lazy('index')
