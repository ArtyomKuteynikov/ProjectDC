from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'password', 'phone', 'gender', 'telegram', 'birthday', 'city',
                  'job_city', 'grade']


class LoginForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['email', 'password']
        widgets = {
            "email": forms.TextInput(attrs={'autocomplete': 'on'}),
            "password": forms.PasswordInput(),
        }


class ChangePassword(forms.Form):
    customer = forms.IntegerField()
    password = forms.CharField()
    new_password = forms.CharField()
