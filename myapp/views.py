from django.shortcuts import render
from django.http import HttpResponse
from .forms import TutorForm

# SHERRIFF: very basic index page created
def index(request):
    return HttpResponse("This is our tutor me project")

def submit_listing(request):
    form = TutorForm(request.POST or None)
    
    if form.is_valid():
        form.save()
    
    context = {
        'form': form
    }
    return render(request, 'myapp/submit_listing.html', context)
