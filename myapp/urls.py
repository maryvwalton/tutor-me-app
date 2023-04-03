from django.urls import path

from . import views

from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', TemplateView.as_view(template_name="myapp/index.html")),
    path('profile/', TemplateView.as_view(template_name="myapp/profile.html")),
    path('submit_listing/', views.submit_listing, name = "submit_listing"),
    path('tutor_courses/', views.listing_view, name = "listing_view"),
    path('add_student_to_listing/', views.update_listing, name = "update_listing"),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view()),
    path('search_classes', views.search_classes, name = 'search-classes')
]