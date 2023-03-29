from django.forms import HiddenInput, ModelChoiceField, ModelForm
from .models import *

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

# class RequestForm(ModelForm):
#     request_form = RequestForm1()

#     class Meta:
#         model = Profile
#         fields = ['user']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if self.instance.pk:
#             self.request_form = RequestForm(instance=self.instance.request)

#         self.fields['sessionRequests'] = ModelChoiceField(queryset=SessionRequest.objects.all(),
#                                                         widget=HiddenInput())

#     def save(self, commit=True):
#         request = self.request_form.save(commit=False)
#         request.save()

#         profile = super().save(commit=False)
#         profile.request = request

#         if commit:
#             profile.save()
#             self.request_form.save_m2m()

#         return profile

#form that students use to add themselves to listing
class UpdateForm(ModelForm):
    class Meta:
        model = SessionRequest

        fields = [
            'student',
        ]
        

        

