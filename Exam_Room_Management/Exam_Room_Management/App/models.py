from django.db import models

class Room(models.Model):
    roomID = models.CharField(max_length=10)
    size = models.IntegerField()
    
"""
class Subject(models.Model):
    subID = models.CharField(max_length=20)
    subName = models.CharField(max_length=20)    
"""
class Student(models.Model):
    stdID = models.CharField(max_length=20)
    stdName = models.CharField(max_length=50)
    