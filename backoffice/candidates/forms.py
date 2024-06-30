from django import forms
from .models import Education, Experience

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['university_name', 'faculty', 'spec_id', 'end_year']

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['company', 'position', 'additional_info', 'start_date', 'end_date']