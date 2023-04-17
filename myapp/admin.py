from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Course)
admin.site.register(Tutor)
admin.site.register(Student)
admin.site.register(SessionRequest)
admin.site.register(Review)
admin.site.register(discussionReplies)
admin.site.register(discussionThread)