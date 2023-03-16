from django.forms import ModelForm
from .models import Tutor

class TutorForm(ModelForm):
    class Meta:
        model = Tutor
        fields = [
            'first_name',
            'last_name',
            'course',
            'hourly_rate',
            # 'user',
        ]
        

