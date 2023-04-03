from django import forms
from django.forms import ModelForm
from .models import SessionRequest,Tutor

#form that tutors use to create a listing
class TutorForm(ModelForm):
    class Meta:
        model = Tutor

        fields = [
            # 'user', 
    'first_name',
    'last_name',
    'course',
    'headline',
    'qualifications',
    'hourly_rate', 
    'rating'
 
        ]

#form that students use to request a tutor
class RequestForm(ModelForm):
    class Meta:
        model = SessionRequest

        fields = [
            'date',
            'start_time',
            'end_time',
            'tutor',
            # 'student',
            'course',
            'service',
 
        ]

#form that students use to add themselves to listing
class UpdateForm(ModelForm):
    class Meta:
        model = SessionRequest

        fields = [
            'student',
        ]

class FilterForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)

        

