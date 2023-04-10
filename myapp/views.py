
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from .forms import TutorForm, RequestForm, FilterForm
from .models import Tutor, SessionRequest

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

#Shows all session requests in tutor_courses.html
def request_view(request):
    sessions = SessionRequest.objects.all()

    args = {'sessions': sessions}

    return render(request, 'myapp/tutor_courses.html', args)


#view that tutors use to make a listing
def submit_listing(request):
    form = TutorForm(request.POST or None, 
                     initial={
        'date': '3/17/23',
        'start_time': '10:00',
        'end_time': '11:00',

        })
    user = request.user
    form.initial['user'] = user

    field = form.fields['user']
    field.widget = field.hidden_widget()

#making the form save the data and also create the slug value by calling save() on it
    if form.is_valid():
        # text = form.cleaned_data['text']
        new_listing = form.save()
        new_listing.save()
    
        # form.save()
        return redirect('/myapp/tutor_courses/')
    
    context = {
        'form': form
    }
    return render(request, 'myapp/submit_listing.html', context)



def search_classes(request):
    if request.method == "POST":
        searched = request.POST.get('searched', default="")
        courses = Tutor.objects.filter(course__title__contains=searched)
        courses2 = Tutor.objects.filter(course__pnemonic__contains=searched)
        courses3 = Tutor.objects.filter(course__coursenum__contains=searched)
    return render(request, 'myapp/search_classes.html', {'searched': searched, 'courses': courses, 'courses2': courses2, 'courses3': courses3})

# View that students use to make a request on a listing
def update_listing(request, pk):

    user = request.user
    tutor = Tutor.objects.get(pk = pk)

    form = RequestForm(request.POST or None)

    form.initial['tutor'] = tutor.id
    form.initial['course'] = tutor.course
    form.initial['student'] = user

    field = form.fields['tutor']
    field.widget = field.hidden_widget()
    field = form.fields['course']
    field.widget = field.hidden_widget()
    field = form.fields['student']
    field.widget = field.hidden_widget()

    if form.is_valid():
        form.save()

        return redirect('/myapp/profile/')
    context = {
        'form': form,
        'tutor':tutor

    }
    return render(request, 'myapp/add_student_to_listing.html', context)


#view that shows the listings associated with a user on the profile page
def filter(request):
    tutor = Tutor.objects.filter(user =request.user)
    sess_request = SessionRequest.objects.filter(tutor__user= request.user)

    sess_request_pending = sess_request.filter(pending__isnull = True)
    sess_request_confirmed = sess_request.filter(pending = 1)

    sess_request_student_side = SessionRequest.objects.filter(student= request.user)

    return render(request, 'myapp/profile.html', {'tutor': tutor, 
                                                  'sess_request': sess_request_pending, 
                                                  'sess_request_student_side': sess_request_student_side,
                                                  'sess_request_confirmed': sess_request_confirmed,})

#view that is used to delete session requests in profile page
def delete_model(request, pk):
    obj = get_object_or_404(SessionRequest, pk=pk)
    if request.method == "POST":
        obj.delete()
        return redirect("/myapp/profile/")
    context = {
        "object": obj
    }

    return render(request, "myapp/profile.html", context)

#view that is used to confirm session requests in profile page
def confirm_model(request, pk):
    obj = get_object_or_404(SessionRequest, pk=pk)
    if request.method == "POST":
        obj.pending = 1
        obj.save()
        return redirect("/myapp/profile/")
    context = {
        "object": obj
    }

    return render(request, "myapp/profile.html", context)

#view that is used to Decline session requests in profile page
def decline_model(request, pk):
    obj = get_object_or_404(SessionRequest, pk=pk)
    if request.method == "POST":
        obj.pending = 2
        obj.save()
        return redirect("/myapp/profile/")
    context = {
        "object": obj
    }

    return render(request, "myapp/profile.html", context)
    



# def filter(request):
#     tutor = Tutor.objects.all()
#     sess_request = SessionRequest.objects.all()
#     form = FilterForm(request.GET or None)
#     if form.is_valid():
#         name = form.cleaned_data.get('name')

#         if name:
#             tutor = tutor.filter(first_name__icontains= name)
#             sess_request = sess_request.filter(tutor__icontains=name)
       
#     return render(request, 'myapp/profile.html', {'form': form, 'tutor': tutor, sess_request: 'sess_request'})



#create discussion thread 
def createThread(request):
    if request.method == 'POST':
        user = request.POST["username"]
        title = request.POST["title_text"]
        question = request.POST["question_text"]
        new_thread = discussionThread(username = user, title_text = title, question_text = question, pub_date = timezone.now())
        new_thread.save()
        return HttpResponseRedirect('/discussion')
    else:
        d = discussionThread()
        return render(request, 'myapp/submitthread.html', {'discussionThread': discussionThread})



#display active threads 
def threadList(request):
    all_threads = discussionThread.objects.all()
    return render(request, 'myapp/discussionthreadlist.html', {'all_threads': all_threads})



