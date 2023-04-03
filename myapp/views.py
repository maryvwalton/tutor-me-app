from email.policy import default
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import TutorForm, RequestForm, FilterForm
from .models import Tutor, SessionRequest
from django.views.generic import DetailView


from myapp.query_SIS_API import *

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
    listing = Tutor.objects.get(id = pk)

    form = TutorForm(request.POST or None, instance = listing)

    if form.is_valid():
        form.save()
        return redirect('/myapp/tutor_courses/')
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
        return redirect('/myapp/tutor_courses/')
    
    context = {
        'form': form
    }
    return render(request, 'myapp/submit_listing.html', context)

def search_classes(request):
    if request.method == "POST":
        searched = request.POST.get('searched', default="")
        courses = Tutor.objects.filter(course__title__contains=searched)
    return render(request, 'myapp/search_classes.html', {'searched': searched, 'courses': courses})

# View that students use to make a request on a listing
def update_listing(request):

    form = RequestForm(request.POST or None)

    if form.is_valid():
        form.save()

        return redirect('/myapp/profile/')
    context = {
        'form': form
    }
    return render(request, 'myapp/add_student_to_listing.html', context)



def filter(request):
    tutor = Tutor.objects.all()
    sess_request = SessionRequest.objects.all()
    form = FilterForm(request.GET or None)
    if form.is_valid():
        name = form.cleaned_data.get('name')

        if name:
            tutor = tutor.filter(first_name__icontains= name)
            sess_request = sess_request.filter(tutor__icontains=name)
       
    return render(request, 'myapp/profile.html', {'form': form, 'tutor': tutor, sess_request: 'sess_request'})
