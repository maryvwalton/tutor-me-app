from django.urls import path

from . import views

from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html")),
    path('profile/', TemplateView.as_view(template_name="profile.html")),
    path('submit_listing/', TemplateView.as_view(template_name="submit_listing.html")),
    path('tutor_courses/', TemplateView.as_view(template_name="tutor_courses.html")),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view()),
]