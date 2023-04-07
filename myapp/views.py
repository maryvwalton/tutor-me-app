
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse

from .forms import TutorForm, RequestForm, FilterForm
from .models import Tutor, SessionRequest
from django.views import generic 

from .forms import TutorForm, UpdateForm, RequestForm
from .models import Tutor, discussionThread, discussionReplies, SessionRequest
from django.utils import timezone
from django.http import Http404, HttpResponse, HttpResponseRedirect


from email.policy import default


from myapp.query_SIS_API import *


# SHERRIFF: very basic index page created


def index(request):
    return HttpResponse("This is our tutor me project")


#View that shows the listings on tutor_courses.html
def listing_view(request):
    listings = Tutor.objects.all()

    args = {'listings': listings}

    return render(request, 'myapp/tutor_courses.html', args)

def request_view(request):
    sessions = SessionRequest.objects.all()

    args = {'sessions': sessions}

    return render(request, 'myapp/tutor_courses.html', args)

#view that students use to add themselves to the SessionRequest model

# def update_listing(request, pk):
#     listing = Tutor.objects.get(id = pk)

#     form = TutorForm(request.POST or None, instance = listing)

#     if form.is_valid():
#         form.save()
#         return redirect('/myapp/tutor_courses/')
#     context = {
#         'form': form
#     }
#     return render(request, 'myapp/add_student_to_listing.html', context)

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


def update_listing(request):

    form = RequestForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('/myapp/tutor_courses/')
    context = {
        'form': form
    }
    return render(request, 'myapp/add_student_to_listing.html', context)

def search_classes(request):
    if request.method == "POST":
        searched = request.POST.get('searched', default="")
        courses = Tutor.objects.filter(course__title__contains=searched)
        courses2 = Tutor.objects.filter(course__pnemonic__contains=searched)
        courses3 = Tutor.objects.filter(course__coursenum__contains=searched)
    return render(request, 'myapp/search_classes.html', {'searched': searched, 'courses': courses, 'courses2': courses2, 'courses3': courses3})

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



#detail view for discussion thread 
class discussionView(generic.DetailView):
    model = discussionThread
    template_name = 'myapp/discussiondetail.html'
    context_object_name = 'thread'


#class based function -- ignore 
# def discussionDetail(request, id):
#     disc = get_object_or_404(discussionThread, pk = id)
#     context = {'disc': disc}
#     return render(request, 'myapp/discussiondetail.html', context)


#create discussion thread 
def createThread(request):
    if request.method == 'POST':
        user = request.POST["username"]
        title = request.POST["title_text"]
        question = request.POST["question_text"]
        new_thread = discussionThread(username = user, title_text = title, question_text = question)
        new_thread.save()
        id = new_thread.pk
        return redirect('thread-detail', pk = new_thread.pk)
    else:
        d = discussionThread()
        return render(request, 'myapp/submitthread.html', {'discussionThread': discussionThread})



#display active threads 
def threadList(request):
    all_threads = discussionThread.objects.all()
    return render(request, 'myapp/discussionthreadlist.html', {'all_threads': all_threads})



#reply to thread 
def replyThread(request, discussionThread_id):
    discussion = get_object_or_404(discussionThread, pk = discussionThread_id)
