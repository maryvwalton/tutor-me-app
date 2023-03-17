from django.forms import ModelForm
from .models import SessionRequest

#form that tutors use to create a listing
class TutorForm(ModelForm):
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
        

