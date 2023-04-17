import datetime

from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify


# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=200)
    pnemonic = models.CharField(max_length=100)
    coursenum = models.IntegerField()

    def __str__(self):

        return self.pnemonic + " " + str(self.coursenum) + " " + self.title
    

class Review(models.Model):
    tutor = models.ForeignKey('Tutor', on_delete=models.CASCADE, related_name="tutorreviews")
    #student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="studentreviews")
    session = models.ForeignKey('SessionRequest', on_delete=models.CASCADE, related_name="sessionsforreview")
    rating = models.FloatField(default=0)
    comment = models.CharField(max_length=300)

    def __str__(self):
         return self.comment



class Tutor(models.Model):
    first_name = models.CharField(max_length=200)  
    last_name = models.CharField(max_length=200)  
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    headline = models.CharField(max_length=300)
    qualifications = models.CharField(max_length=750)
    hourly_rate = models.FloatField(default=0)
    rating = models.FloatField(default=0)

    def __str__(self):
        return self.first_name + self.last_name
    
    def save(self, *args, **kwargs):
        # self.slug = slugify(self.first_name)
        super(Tutor, self).save(*args, **kwargs)

    #sign up form to become a tutor 



class Student(models.Model):
    first_name = models.CharField(max_length=200, default = "Bobby")  
    last_name = models.CharField(max_length=200, default = "Brown")  
    #submit request function

    def __str__(self):
        return self.first_name + self.last_name



class SessionRequest(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    service_choices = (
    ("1", "General subject review"),
    ("2", "Homework/Practice problem help"),
    ("3", "Exam Prep"),
    ("4", "Other")
)
    service = models.CharField(max_length=150, choices = service_choices)

    pending_choices = (
        (1, 'Confirm'),
        (2, 'Decline'),
    )
    pending = models.IntegerField(choices= pending_choices, null= True)

    def __str__(self):
        return str(self.date) + " " + str(self.course) 
    
    

# class Profile(models.Model):
#     user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
#     tutorSubmissions = models.ForeignKey(Tutor, on_delete=models.CASCADE, default=1)
#     sessionRequests = models.ForeignKey(SessionRequest, on_delete=models.CASCADE, default = 1)

#     def __str__(self):
#         return str(self.user)


class Profile(models.Model):
    user = models.OneToOneField(User, null = True, on_delete = models.CASCADE)

    def __str__(self):
        return str(self.user)


class discussionThread(models.Model):
    username = models.CharField(max_length=200)  
    title_text = models.CharField(max_length=200, null = True)
    question_text = models.CharField(max_length=500)
    #pub_date = models.DateTimeField(timezone.now(), null = True)

    def __str__(self):
         return self.question_text

class discussionReplies(models.Model):
    username = models.CharField(max_length=200) 
    reply_text = models.CharField(max_length=500)
    question = models.ForeignKey(discussionThread, on_delete=models.CASCADE, related_name="replies")
    #reply_date = models.DateTimeField(timezone.now(), null = True)

    def __str__(self):
         return self.objects.count()

    def count_replies(self): 
        return self.objects.count()

