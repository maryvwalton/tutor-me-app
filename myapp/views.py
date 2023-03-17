from django.shortcuts import render
from django.http import HttpResponse
from .forms import TutorForm, UpdateForm
from .models import Tutor

# SHERRIFF: very basic index page created

def index(request):
    return HttpResponse("This is our tutor me project")


#View that shows the listings on tutor_courses.html
def listing_view(request):
    listings = Tutor.objects.all()

    args = {'listings': listings}

    return render(request, 'myapp/tutor_courses.html', args)

#view that students use to add themselves to the SessionRequest model
def update_listing(request, pk):
    form = UpdateForm(request.POST or None)
    
    if form.is_valid():
        form.save()
    
    context = {
        'form': form
    }
    return render(request, 'myapp/add_student_to_listing.html', context)

#view that tutors use to make a listing
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
