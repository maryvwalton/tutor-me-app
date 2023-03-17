from django.forms import ModelForm
from .models import SessionRequest

class TutorForm(ModelForm):
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
        

