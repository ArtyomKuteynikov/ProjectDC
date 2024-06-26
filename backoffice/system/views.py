from os import getenv
from random import randint

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache

from .models import Customer, City, Grade, Spec
from .forms import CustomerForm, LoginForm, ChangePassword
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
        customer = Customer.objects.filter(email=email)
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


@csrf_exempt
def restore_password(request):
    if request.headers['SECRET-SYSTEM'] != getenv('SECRET_SYSTEM'):
        return HttpResponse({'status': False}, status=403)
    email = request.GET['email']
    print(email)
    customer = Customer.objects.filter(email=email).first()
    if not customer:
        return HttpResponse({'status': False}, status=404)
    number = randint(100000, 999999)
    cache.set(f'code:{email}', number, timeout=3600*600)
    text = f'''Добрый день!
    
Ваш код сброса пароля: {number}

С уважением,
JoinHub
'''
    send_email(email, "Сброс пароля", text)
    return JsonResponse(data={'status': True}, status=200)


@csrf_exempt
def enter_code(request):
    if request.headers['SECRET-SYSTEM'] != getenv('SECRET_SYSTEM'):
        return HttpResponse({'status': False}, status=403)
    email = request.GET['email']
    code = request.GET['code']
    print(str(code) != str(cache.get(f'code:{email}')), str(code), str(cache.get(f'code:{email}')))
    if str(code) != str(cache.get(f'code:{email}')):
        return HttpResponse({'status': False}, status=400)
    customer = Customer.objects.all().filter(email=email).first()
    if not customer:
        return HttpResponse({'status': False}, status=404)
    return JsonResponse(data={'status': True, 'user': customer.id}, status=200)


@csrf_exempt
def change_password(request):
    if request.method == 'POST':
        form = ChangePassword(request.POST)
        if request.headers['SECRET-SYSTEM'] != getenv('SECRET_SYSTEM'):
            return HttpResponse({'status': False}, status=403)
        if not form.is_valid():
            return HttpResponse({'status': False}, status=400)
        if form.password != form.new_password:
            return HttpResponse({'status': False}, status=400)
        customer = Customer.objects.all().filter(id=form.customer).first()
        if not customer:
            return HttpResponse({'status': False}, status=404)
        customer.set_password_hash(form.password)
        return JsonResponse(data={'status': True, 'user': customer.id}, status=200)
    else:
        return HttpResponse({'status': False}, status=405)

@csrf_exempt
def cities_list(request):
    cities = City.objects.all()
    return JsonResponse(data={'cities': [{'id': city.id, 'name': city.name} for city in cities]}, status=200)

@csrf_exempt
def grades_list(request):
    grades = Grade.objects.all()
    return JsonResponse(data={'grades': [{'id': grade.id, 'name': grade.name} for grade in grades]}, status=200)

@csrf_exempt
def specs_list(request):
    specs = Spec.objects.all()
    return JsonResponse(data={'specs': [{'id': spec.id, 'name': spec.name} for spec in specs]}, status=200)
