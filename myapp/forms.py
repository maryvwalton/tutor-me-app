
from django import forms
from django.forms import HiddenInput, ModelChoiceField, ModelForm
from .models import *


#form that tutors use to create a listing
class TutorForm(ModelForm):
    class Meta:
        model = Tutor

        fields = [
    'user', 
    'first_name',
    'last_name',
    'course',
    'headline',
    'qualifications',
    'hourly_rate', 
 
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
            'student',
            'course',
            'service',
 
        ]

#form that tutors use to confirm/regect session requests
class PendingForm(ModelForm):
    class Meta:
        model = SessionRequest
        fields = [
            'pending',
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

        
#discussion response form 
class ReplyForm(ModelForm):
    class Meta:
        model = discussionReplies
        fields = [
            'username',
            'reply_text',
            #'question',
        ]
        

