# тут должны быть все view функции связанные с регистрацией и аутентификацией

from django.shortcuts import render
from django.views import View
from .models import Customer
from .forms import CustomerForm, LoginForm
from os import getenv
from random import randint
from .utils import send_email


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'system/index.html')


def register(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if request.POST['SECRET_KEY'] != getenv('SECRET_SYSTEM'):
            return render(request, 'system/registration.html', {'form': form, 'messages': ['Несовпадение секретных ключей!']}, status=403)
        if form.is_valid():
            email = form.cleaned_data['email']
            customer = Customer.objects.all().filter(email=email)
           
            if len(customer) > 0:
                form.add_error(None, 'Данный email уже зарегистрирован')
                return render(request, 'system/registration.html', {'form': form, 'success': False}, status=400)
            else:
                form.save()
                return render(request, 'system/index.html', {'form': form, 'success': True}, status=200)
    else:
        form = CustomerForm()
    return render(request, 'system/registration.html', {'form': form}) 

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if request.POST['SECRET_KEY'] != getenv('SECRET_SYSTEM'):
            return render(request, 'system/login.html', {'form': form, 'messages': ['Несовпадение секретных ключей!']}, status=403)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            customer = Customer.objects.all().filter(email=email)
           
            if len(customer) == 0:
                form.add_error(None, 'Аккаунт с таким email не зарегистрирован')
                return render(request, 'system/login.html', {'form': form, 'success': False}, status=401)
            
            customer = customer[0]
            if password != customer.password:
                form.add_error(None, 'Введён неверный пароль')
                return render(request, 'system/login.html', {'form': form, 'success': False}, status=401)
            else:
                return render(request, 'system/index.html', {'form': form, 'success': True}, status=200)
    else:
        form = LoginForm()
    return render(request, 'system/login.html', {'form': form})

def restore_password(request):
    if request.method == 'POST':
        if request.POST['SECRET_KEY'] != getenv('SECRET_SYSTEM'):
            return render(request, 'system/restore_password.html', {'messages': ['Несовпадение секретных ключей!']}, status=403)
        email = request.POST['email']
        customer = Customer.objects.all().filter(email=email)

        if len(customer) == 0:
            return render(request, 'system/restore_password.html', {'messages': ['Аккаунт с таким email не зарегистрирован']}, status=401)
        
        number = randint(1000, 9999)
        send_email(email, "Restoring password", str(number))
        return enter_code(request, email, number)
    
    return render(request, 'system/restore_password.html')

def enter_code(request, email, number):
    if request.method == 'POST':
        if request.POST['SECRET_KEY'] != getenv('SECRET_SYSTEM'):
            return render(request, 'system/enter_code.html', {'messages': ['Несовпадение секретных ключей!']}, status=403)

        if request.POST['code'] != number:
            return render(request, 'system/enter_code.html', {'messages': ['Введён неверный код!']}, status=401)
        
        password = request.POST['password']
        
        if password != request.POST['password_again']:
            return render(request, 'system/enter_code.html', {'messages': ['Пароли отличаются']}, status=401)

        Customer.objects.all().filter(email=email)[0].password = password
        return render(request, 'system/login.html', {'success': True}, status=200)
    
    return render(request, 'system/enter_code.html')