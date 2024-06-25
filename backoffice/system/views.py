from os import getenv
from random import randint

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import Customer
from .forms import CustomerForm, LoginForm
from .utils import send_email


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'system/index.html')


@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if request.headers['SECRET-SYSTEM'] != getenv('SECRET_SYSTEM'):
            return HttpResponse({'status': False}, status=403)
        if not form.is_valid():
            return HttpResponse({'status': False}, status=400)
        email = form.cleaned_data['email']
        customer = Customer.objects.all().filter(email=email)
        if len(customer) > 0:
            return HttpResponse({'status': False}, status=400)
        else:
            customer = form.save()
            customer.set_password_hash(customer.password)
            return JsonResponse(data={'status': True, 'user': customer.id}, status=200)
    else:
        return HttpResponse({'status': False}, status=405)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if request.headers['SECRET-SYSTEM'] != getenv('SECRET_SYSTEM'):
            return HttpResponse({'status': False}, status=403)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            customer = Customer.objects.all().filter(email=email).first()
            if not customer:
                return HttpResponse({'status': False}, status=404)
            if not customer.verify_password(password):
                return HttpResponse({'status': False}, status=401)
            else:
                return JsonResponse(data={'status': True, 'user': customer.id}, status=200)
    else:
        return HttpResponse({'status': False}, status=405)


def restore_password(request):
    if request.method == 'POST':
        if request.POST['SECRET_KEY'] != getenv('SECRET_SYSTEM'):
            return render(request, 'system/restore_password.html', {'messages': ['Несовпадение секретных ключей!']},
                          status=403)
        email = request.POST['email']
        customer = Customer.objects.all().filter(email=email)

        if len(customer) == 0:
            return render(request, 'system/restore_password.html',
                          {'messages': ['Аккаунт с таким email не зарегистрирован']}, status=401)

        number = randint(1000, 9999)
        send_email(email, "Restoring password", str(number))
        return enter_code(request, email, number)

    return render(request, 'system/restore_password.html')


def enter_code(request, email, number):
    if request.method == 'POST':
        if request.POST['SECRET_KEY'] != getenv('SECRET_SYSTEM'):
            return render(request, 'system/enter_code.html', {'messages': ['Несовпадение секретных ключей!']},
                          status=403)

        if request.POST['code'] != number:
            return render(request, 'system/enter_code.html', {'messages': ['Введён неверный код!']}, status=401)

        password = request.POST['password']

        if password != request.POST['password_again']:
            return render(request, 'system/enter_code.html', {'messages': ['Пароли отличаются']}, status=401)

        Customer.objects.all().filter(email=email)[0].password = password
        return render(request, 'system/login.html', {'success': True}, status=200)

    return render(request, 'system/enter_code.html')
