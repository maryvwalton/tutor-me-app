import datetime

from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

# Create your models here.


class Course(models.Model):
    title = models.CharField(max_length=200)
    pnemonic = models.CharField(max_length=100)
    coursenum = models.IntegerField()

    def __str__(self):
        return self.pnemonic + " " + str(self.coursenum)+ " " + self.title

class Tutor(models.Model):
    first_name = models.CharField(max_length=200)  
    last_name = models.CharField(max_length=200)  
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    headline = models.CharField(max_length=300)
    qualifications = models.CharField(max_length=750)
    hourly_rate = models.FloatField(default=0)
    rating = models.FloatField(default=0)

    #sign up form to become a tutor 

    def __str__(self):
        return self.first_name + self.last_name


class Student(models.Model):
    first_name = models.CharField(max_length=200)  
    last_name = models.CharField(max_length=200)  


    #submit request function

    def __str__(self):
        return self.first_name + self.last_name


class SessionRequest(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    service = models.CharField(max_length=150)

    def __str__(self):
        return str(self.id)
    

class Review(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.OneToOneField(SessionRequest, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)
    comment = models.CharField(max_length=300)

    def __str__(self):
         return self.comment
