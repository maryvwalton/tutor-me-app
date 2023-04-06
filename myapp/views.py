
from django.shortcuts import redirect, render, reverse
from django.http import HttpResponse
from django.urls import reverse_lazy

from .forms import TutorForm, RequestForm, FilterForm
from .models import Tutor, SessionRequest
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
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

    tutor = Tutor.objects.get(pk = pk)

    form = RequestForm(request.POST or None)

    form.initial['tutor'] = tutor.id
    form.initial['course'] = tutor.course

    field = form.fields['tutor']
    field.widget = field.hidden_widget()
    field = form.fields['course']
    field.widget = field.hidden_widget()

    if form.is_valid():
        form.save()

        return redirect('/myapp/profile/')
    context = {
        'form': form,
        'tutor':tutor

    }
    return render(request, 'myapp/add_student_to_listing.html', context)




# class SessionRequestView(FormMixin, DetailView):
#     model = Tutor
#     form_class = RequestForm

#     def get_success_url(self):
#         return reverse('update_listing', kwargs={'tutor_id': self.object.tutor_id})


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['form'] = self.get_form()
    #     context['comments'] = BookComment.objects.filter(
    #         book=self.object).order_by('-id')
    #     return context

    # def post(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated:
    #         return HttpResponseForbidden()
    #     self.object = self.get_object()
    #     form = self.get_form()
    #     if form.is_valid():
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)

    # def form_valid(self, form):
    #     b = self.get_object()
    #     text = form.cleaned_data['text']
    #     new_comment = BookComment(text=text, book=b, user=self.request.user)
    #     new_comment.save()
    #     messages.success(self.request, "Your comment is added, thank you")
    #     return super().form_valid(form)



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



