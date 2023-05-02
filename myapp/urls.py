from django.urls import path

from . import views
# from .views import (SessionRequestView) 

from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', TemplateView.as_view(template_name="myapp/index.html")),
    path('submit_listing/', views.submit_listing, name="submit_listing"),

    path('submit_listing/add_more_availability/<int:pk>', views.add_more_availability, name="add_more_availability"),

    path('tutor_courses/', views.listing_view, name="listing_view"),
    path('add_student_to_listing/<int:pk>', views.update_listing, name="update_listing"),
    path('remove_availability/<int:pk>/<command>', views.remove_appointment_when_booked,
         name="remove_appointment_when_booked"),

    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view()),
    path('search_classes', views.search_classes, name='search-classes'),

    path('profile/', views.filter, name='filter'),
    path('discussion', views.threadList, name='threadslist'),

    path('delete/<int:pk>/', views.delete_model, name='delete_model'),
    path('confirm/<int:pk>/', views.confirm_model, name='confirm_model'),
    path('decline/<int:pk>/', views.decline_model, name='decline_model'),
    path('search_discussions', views.search_discussions, name = 'search_discussions'),

    path('discussion/<int:pk>', views.discussionView.as_view(), name='discussionThread'),
    path('discussion/<int:discussionThread_id>/reply', views.replyThread, name='replyThread'),
    path('submit_thread/', views.createThread, name = 'submitthread'),
    path('submit_review/<int:pk>', views.submitReview, name = 'submitreview'),
    path('review_detail/<int:pk>', views.reviewView.as_view(), name = 'viewReview'),
    path('reviews', views.reviewList, name = 'allreviews'),
    path('reviews/<int:id>', views.tutorReview, name = 'tutor_review'), 

]