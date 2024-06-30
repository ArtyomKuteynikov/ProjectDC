# тут должны быть все view функции связанные с резюме(CRUD, каталог, фильтр)

from os import getenv

from system.models import Customer, Grade, City, Spec
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from system.forms import CustomerForm

from .models import Education, Experience
from .forms import EducationForm, ExperienceForm

@csrf_exempt
def customer_info(request):
    profile_id = request.GET.get('id')
    customer = Customer.objects.filter(id=profile_id)
    city = City.objects.filter(id=customer.city)
    job_city = City.objects.filter(id=customer.job_city)
    grade = Grade.objects.filter(id=customer.grade)
    return JsonResponse(data={'first_name': customer.first_name, 'last_name': customer.last_name, 'email': customer.email, 'phone': customer.phone, 'gender': customer.gender,
                              'telegram': customer.telegram, 'birthday': customer.birthday, 'city': city.name, 'job_city': job_city.name, 'grade': grade.name, 'role': customer.role}, status=200)

@csrf_exempt
def education_list_info(request):
    user_id = request.GET.get('id')
    education = Education.objects.all().filter(id=user_id)
    return JsonResponse(data={'education': [{'university_name': university.university_name, 'faculty': university.faculty,
                                             'spec': Spec.objects.filter(id=university.spec_id).name, 'end_year': university.end_year}] for university in education}, status=200)

@csrf_exempt
def experience_list_info(request):
    user_id = request.GET.get('id')
    all_experience = Experience.objects.all().filter(id=user_id)
    return JsonResponse(data={'experience': [{'company': experience.company, 'position': experience.position, 'additional_info': experience.additional_info,
                                              'start_date': experience.start_date, 'end_date': experience.end_date}] for experience in all_experience}, status=200)

@csrf_exempt
def education_info(request):
    university_id = request.GET.get('id')
    university = Education.objects.filter(id=university_id)
    return JsonResponse(data={'university_name': university.university_name, 'faculty': university.faculty,
                                             'spec': Spec.objects.filter(id=university.spec_id).name, 'end_year': university.end_year}, status=200)

@csrf_exempt
def experience_info(request):
    experience_id = request.GET.get('id')
    experience = Experience.objects.filter(id=experience_id)
    return JsonResponse(data={'company': experience.company, 'position': experience.position, 'additional_info': experience.additional_info,
                                              'start_date': experience.start_date, 'end_date': experience.end_date}, status=200)

@csrf_exempt
def add_education(request):
    customer_id = request.GET.get('id')
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if request.headers['SECRET-SYSTEM'] != getenv('SECRET_SYSTEM'):
            return HttpResponse({'status': False}, status=403)
        if not form.is_valid():
            return HttpResponse({'status': False}, status=400)
        education = form.save()
        education.user_id = customer_id
        education.save()
        return JsonResponse(data={'status': True, 'education': education.id}, status=200)

@csrf_exempt
def add_experience(request):
    customer_id = request.GET.get('id')
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if request.headers['SECRET-SYSTEM'] != getenv('SECRET_SYSTEM'):
            return HttpResponse({'status': False}, status=403)
        if not form.is_valid():
            return HttpResponse({'status': False}, status=400)
        experience = form.save()
        experience.user_id = customer_id
        experience.save()
        return JsonResponse(data={'status': True, 'experience': experience.id}, status=200)

@csrf_exempt
def customer_update(request):
    customer = get_object_or_404(Customer, pk=request.GET.get('id'))
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
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
def education_update(request):
    education = get_object_or_404(Education, pk=request.GET.get('id'))
    if request.method == 'POST':
        form = EducationForm(request.POST, instance=education)
        if request.headers['SECRET-SYSTEM'] != getenv('SECRET_SYSTEM'):
            return HttpResponse({'status': False}, status=403)
        if not form.is_valid():
            return HttpResponse({'status': False}, status=400)
        education = form.save()
        return JsonResponse(data={'status': True, 'education': education.id}, status=200)
    else:
        return HttpResponse({'status': False}, status=405)

@csrf_exempt
def experience_update(request):
    experience = get_object_or_404(Experience, pk=request.GET.get('id'))
    if request.method == 'POST':
        form = ExperienceForm(request.POST, instance=experience)
        if request.headers['SECRET-SYSTEM'] != getenv('SECRET_SYSTEM'):
            return HttpResponse({'status': False}, status=403)
        if not form.is_valid():
            return HttpResponse({'status': False}, status=400)
        experience = form.save()
        return JsonResponse(data={'status': True, 'experience': experience.id}, status=200)
    else:
        return HttpResponse({'status': False}, status=405)

@csrf_exempt
def customer_delete(request):
    customer = get_object_or_404(Customer, pk=request.GET.get('id'))
    customer.delete()
    return JsonResponse(data={'status': True}, status=200)

@csrf_exempt
def education_delete(request):
    education = get_object_or_404(Education, pk=request.GET.get('id'))
    education.delete()
    return JsonResponse(data={'status': True}, status=200)

@csrf_exempt
def experience_delete(request):
    experience = get_object_or_404(Experience, pk=request.GET.get('id'))
    experience.delete()
    return JsonResponse(data={'status': True}, status=200)