from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from .forms import TutorForm, RequestForm, FilterForm, AppointmentForm
from .models import Tutor, SessionRequest, Review, User, Appointment

from django.views import generic
from .forms import TutorForm, UpdateForm, RequestForm, ReplyForm
from .models import Tutor, discussionThread, discussionReplies, SessionRequest
from django.utils import timezone
from django.http import Http404, HttpResponse, HttpResponseRedirect

from django.db.models import Count, Avg, Prefetch, Func

from email.policy import default


# SHERRIFF: very basic index page created


def index(request):
    return HttpResponse("This is our tutor me project")


class Round(Func):
    function = 'ROUND'
    template='%(function)s(%(expressions)s, 2)'


#View that shows the listings on tutor_courses.html
def listing_view(request):
    
    listings = Tutor.objects.annotate(avg_rating = Round(Avg('tutorreviews__rating')))

    # reviews = Tutor.objects.all().prefetch_related(
    #     Prefetch(
    #         'tutorreviews',
    #         Review.objects.select_related('tutor'),
    #         to_attr = 'specific_reviews'),
    #     )

    args = {'listings': listings}

    return render(request, 'myapp/tutor_courses.html', args)


# Shows all session requests in tutor_courses.html
def request_view(request):
    sessions = SessionRequest.objects.all()

    args = {'sessions': sessions}

    return render(request, 'myapp/tutor_courses.html', args)


def add_more_availability(request, pk):
    form = AppointmentForm(request.POST or None)
    tutor = Tutor.objects.get(pk=pk)

    form.initial['course'] = tutor.course

    if request.method == 'POST':

        if form.is_valid():
            appointment = form.save(commit=False)

            appointment.tutor = tutor
            appointment.save()

    context = {
        'form': form
    }

    return render(request, 'myapp/add_more_availability.html', context)


# view that tutors use to make a listing
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

    current_user_linked_to_tutors = Tutor.objects.filter(user=user).last()
    if current_user_linked_to_tutors:
        # form.initial['first_name'] = current_user_linked_to_tutors.first_name
        # form.initial['last_name'] = current_user_linked_to_tutors.last_name
        form.initial['course'] = current_user_linked_to_tutors.course
        form.initial['headline'] = current_user_linked_to_tutors.headline
        form.initial['qualifications'] = current_user_linked_to_tutors.qualifications
        form.initial['hourly_rate'] = current_user_linked_to_tutors.rating

    # making the form save the data and also create the slug value by calling save() on it
    if form.is_valid():
        # text = form.cleaned_data['text']
        new_listing = form.save(commit=False)

        # trying to eliminate repeats
        check_if_tutor_in_database_query = Tutor.objects.filter(
                                                                # first_name=new_listing.first_name,
                                                                # last_name=new_listing.last_name,
                                                                user=new_listing.user,
                                                                course=new_listing.course,
                                                                headline=new_listing.headline,
                                                                qualifications=new_listing.qualifications,
                                                                hourly_rate=new_listing.hourly_rate,
                                                                rating=new_listing.rating).first()

        if not check_if_tutor_in_database_query:
            new_listing.save()

        appointment = Appointment(date=form.cleaned_data["date"],
                                  start_time=form.cleaned_data["start_time"],
                                  end_time=form.cleaned_data["end_time"],
                                  tutor=(check_if_tutor_in_database_query or Tutor.objects.get(pk=new_listing.pk)),
                                  course=new_listing.course)

        appointment.save()

        # form.save()
        return redirect('add_more_availability', pk=(new_listing.pk or check_if_tutor_in_database_query.pk))

    # field = form.fields['first_name']
    # field.widget = field.hidden_widget()
    # field = form.fields['last_name']
    # field.widget = field.hidden_widget()
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
    return render(request, 'myapp/search_classes.html',
                  {'searched': searched, 'courses': courses, 'courses2': courses2, 'courses3': courses3})


# View that students use to make a request on a listing
# def update_listing(request, pk):
#     user = request.user
#     tutor = Tutor.objects.get(pk=pk)
#
#     form = RequestForm(request.POST or None)
#
#     form.initial['tutor'] = tutor.id
#     form.initial['course'] = tutor.course
#     form.initial['student'] = user
#
#     field = form.fields['tutor']
#     field.widget = field.hidden_widget()
#     field = form.fields['course']
#     field.widget = field.hidden_widget()
#     field = form.fields['student']
#     field.widget = field.hidden_widget()
#
#     if form.is_valid():
#         form.save()
#
#         return redirect('/myapp/profile/')
#
#     context = {
#         'form': form,
#         'tutor': tutor
#
#     }
#     return render(request, 'myapp/add_student_to_listing.html', context)

def remove_appointment_when_booked(request, pk, command):
    tutor_id = Appointment.objects.get(pk=pk).tutor.id

    if command == 'delete':
        appointment_to_delete = Appointment.objects.get(pk=pk)

        new_session = SessionRequest(date=appointment_to_delete.date,
                                                    start_time=appointment_to_delete.start_time,
                                                    end_time=appointment_to_delete.end_time,
                                                    tutor=appointment_to_delete.tutor,
                                                    student=request.user,
                                                    course=appointment_to_delete.course)

        new_session.save()

        appointment_to_delete.delete()

    return redirect("update_listing", pk=tutor_id)


def update_listing(request, pk):
    user = request.user
    tutor = Tutor.objects.get(pk=pk)

    sessions_with_matching_appointments = SessionRequest.objects.filter()
    all_appointments = Appointment.objects.filter(tutor=tutor, course=tutor.course)

    appointments = Appointment.objects.filter(tutor=tutor, course=tutor.course)

    context = {
        'tutor': tutor,
        'appointments': appointments,

    }
    return render(request, 'myapp/add_student_to_listing.html', context)


# view that shows the listings associated with a user on the profile page
def filter(request):
    tutor = Tutor.objects.filter(user=request.user)
    sess_request = SessionRequest.objects.filter(tutor__user=request.user)

    sess_request_pending = sess_request.filter(pending__isnull=True)
    sess_request_confirmed = sess_request.filter(pending=1)

    sess_request_student_side = SessionRequest.objects.filter(student=request.user)

    return render(request, 'myapp/profile.html', {'tutor': tutor,
                                                  'sess_request': sess_request_pending,
                                                  'sess_request_student_side': sess_request_student_side,
                                                  'sess_request_confirmed': sess_request_confirmed,
                                                  'is_tutor': tutor.exists(),
                                                  'has_sess_request': sess_request_pending.exists(),
                                                  'has_sess_request_student_side': sess_request_student_side.exists(),
                                                  'has_sess_request_confirmed': sess_request_confirmed.exists(),
                                                  })


# view that is used to delete session requests in profile page
def delete_model(request, pk):
    obj = get_object_or_404(SessionRequest, pk=pk)
    if request.method == "POST":

        # only add back if the student deletes first, NOT if tutor deletes THEN student deletes

        add_the_appointment_back = Appointment(date=obj.date,
                                                              start_time=obj.start_time,
                                                              end_time=obj.end_time,
                                                              tutor=obj.tutor,
                                                              course=obj.course)

        check_if_appointment_in_db = Appointment.objects.filter(date=obj.date,
                                                              start_time=obj.start_time,
                                                              end_time=obj.end_time,
                                                              tutor=obj.tutor,
                                                              course=obj.course)

        if not check_if_appointment_in_db: # needs work
            print(check_if_appointment_in_db)
            add_the_appointment_back.save()


        obj.delete()
        return redirect("/myapp/profile/")
    context = {
        "object": obj
    }

    return render(request, "myapp/profile.html", context)


# view that is used to confirm session requests in profile page
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


# view that is used to Decline session requests in profile page
def decline_model(request, pk):
    obj = get_object_or_404(SessionRequest, pk=pk)
    if request.method == "POST":
        obj.pending = 2
        obj.save()

        add_the_appointment_back = Appointment(date=obj.date,
                                                              start_time=obj.start_time,
                                                              end_time=obj.end_time,
                                                              tutor=obj.tutor,
                                                              course=obj.course)
        add_the_appointment_back.save()
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


# detail view for discussion thread
class discussionView(generic.DetailView):
    model = discussionThread
    template_name = 'myapp/discussiondetail.html'
    context_object_name = 'thread'



# create discussion thread
def createThread(request):
    if request.method == 'POST':
        user = request.user
        # user = request.POST["username"]
        title = request.POST["title_text"]
        question = request.POST["question_text"]
        new_thread = discussionThread(username=user, title_text=title, question_text=question)
        new_thread.save()
        id = new_thread.pk
        return redirect('discussionThread', pk=new_thread.pk)
    else:
        d = discussionThread()
        return render(request, 'myapp/submitthread.html', {'discussionThread': discussionThread})


# display active threads
def threadList(request):
    all_threads = discussionThread.objects.annotate(num_replies=Count('replies'))
    return render(request, 'myapp/discussionthreadlist.html', {'all_threads': all_threads})


# reply to thread
def replyThread(request, discussionThread_id):
    discussion = get_object_or_404(discussionThread, pk=discussionThread_id)

    if request.method == 'POST':
       user = request.user
    #    user = request.POST["username"]
       text = request.POST["response"]
       thread_question = discussion
       new_reply = discussionReplies(username = user, reply_text = text, question = thread_question)
       new_reply.save()
       return redirect('discussionThread', pk = discussion.pk)

    else:
        r = discussionReplies()
        return render(request, 'myapp/reply_to_thread.html', {'discussionReplies': discussionReplies})


#submit review about tutor  
def submitReview(request):
    tutors_list = Tutor.objects.all()
    student_list = User.objects.all()
    session_list = SessionRequest.objects.all()

    if request.method == 'POST':
        select_tutor = request.POST["tutor"]
        #select_session = request.POST.get("session")
        rating = request.POST["rating"]
        review = request.POST["review_text"]
        new_review = Review(tutor_id = select_tutor, rating = rating, comment = review)
        new_review.save()
        id = new_review.pk
        return redirect('viewReview', pk = new_review.pk)
    else:
        r = Review()
        return render(request, 'myapp/submit_review.html', {'review': Review, 'tutors_list':tutors_list, 
                                                            'student_list':student_list, 'session_list':session_list})


#detail view for review submission
class reviewView(generic.DetailView):
    model = Review
    template_name = 'myapp/review_detail.html'
    context_object_name = 'review'


#display all reviews
def reviewList(request):
    all_reviews = Review.objects.all()
    return render(request, 'myapp/all_reviews.html', {'all_reviews': all_reviews})
