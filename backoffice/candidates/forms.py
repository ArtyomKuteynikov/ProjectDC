from django import forms
from .models import Education, Experience, CV

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['university_name', 'faculty', 'spec_id', 'end_year']

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['company', 'position', 'additional_info', 'start_date', 'end_date']

class CVForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = ['applicant_spec_id', 'description', 'salary_min', 'salary_max']