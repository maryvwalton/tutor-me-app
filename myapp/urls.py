from django.urls import path

from . import views

from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', TemplateView.as_view(template_name="myapp/index.html")),
    path('profile/', TemplateView.as_view(template_name="myapp/profile.html")),
    path('submit_listing/', views.submit_listing, name = "submit_listing"),
    path('tutor_courses/', TemplateView.as_view(template_name="myapp/tutor_courses.html")),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view()),
]