from django.forms import ModelForm
from .models import Customer

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'password', 'phone', 'gender', 'telegram', 'birthday', 'city', 'job_city', 'grade', 'role', 'company']