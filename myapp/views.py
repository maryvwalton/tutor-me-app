from django.shortcuts import render
from django.http import HttpResponse
from .forms import TutorForm
from .models import SessionRequest

# SHERRIFF: very basic index page created
def listing_view(request):
    listings = SessionRequest.objects.all()

    args = {'listings': listings}
    
    return render(request, 'myapp/tutor_courses.html', args)



def index(request):
    return HttpResponse("This is our tutor me project")

def submit_listing(request):
    form = TutorForm(request.POST or None, 
                     initial={
        'date': '3/17/23',
        'start_time': '10:00',
        'end_time': '11:00',

        })

    
    if form.is_valid():
        form.save()
    
    context = {
        'form': form
    }
    return render(request, 'myapp/submit_listing.html', context)
