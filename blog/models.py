from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import *

class Practical(models.Model):
    title = models.CharField(max_length=200)
    link = models.TextField()
    thingsneeded = models.TextField()
    subject_tag = models.TextField()
    year_tag = models.TextField()
    def publish(self):
        self.save()

    def __str__(self):
        return self.title
class Year(models.Model):
    tag = models.CharField(max_length=200)
    def publish(self):
        self.save()

    def __str__(self):
        return self.tag
class Technician(models.Model):
    name = models.CharField(max_length=200)
    subject_tag = models.TextField()
    email = models.TextField()
    def publish(self):
        self.save()

    def __str__(self):
        return str(self.name) + " ("+str(self.email)+")"
class Subject(models.Model):
    title = models.CharField(max_length=200)
    tag = models.CharField(max_length=200)
    def publish(self):
        self.save()
        
    def __str__(self):
        return self.title
class Calendar(models.Model):
    datetime = models.CharField(max_length=200)
    room = models.CharField(max_length=200)
    practical = models.CharField(max_length=200)
    technician = models.CharField(max_length=200)
    teacher = models.CharField(max_length=200)
    sets = models.CharField(max_length=200)
    prints = models.CharField(max_length=200)
    def publish(self):
        self.save()

    def __str__(self):
        return self.technician
class Period(models.Model):
    title = models.CharField(max_length=200)
    time = models.CharField(max_length=200)
    def publish(self):
        self.save()

    def __str__(self):
        return str(self.title) + " ("+str(self.time)+")"
