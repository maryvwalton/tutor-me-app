import datetime

from django.db import models
from django.contrib import admin


# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=200)  
    first_name = models.CharField(max_length=200)  
    last_name = models.CharField(max_length=200)  
    email = models.EmailField(max_length=200, unique=True)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.username
    

class Tutor(models.Model):
    user = models.OneToOneField(User)
    course = models.ManyToManyField(Course, blank=True)
    headline = models.CharField(max_length=300)
    qualifications = models.CharField(max_length=750)
    hourly_rate = models.FloatField(default=0)
    rating = models.FloatField(default=0)

    def __str__(self):
        return self.user.username 


class Student(models.Model):
    user = models.OneToOneField(User)

    def __str__(self):
        return self.user.username 


class Course(models.Model):
    title = models.CharField(max_length=200)
    pnemonic = models.CharField(max_length=100)
    professor = models.CharField(max_length=200)

    def __str__(self):
        return self.title
    
    
class SessionRequest(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    service = models.CharField(max_length=150)

    def __str__(self):
        return str(self.id) + self.student.user.username + self.tutor.user.username
    

class Review(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.OneToOneField(SessionRequest, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)
    comment = models.CharField(max_length=300)

    def __str__(self):
         return self.comment
