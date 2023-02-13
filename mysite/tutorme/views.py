from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the Team A-30 group project.")
