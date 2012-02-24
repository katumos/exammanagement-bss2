from django.db import models

class ExamRoom(models.Model):
    roomID = models.CharField(max_length=10)    
    subA = models.CharField(max_length=20)
    subB = models.CharField(max_length=20)
    size = models.IntegerField()
    seatA = []
    seatB = []
    
    def isSeatAFull(self):
        return ( self.seatA.__len__() == self.size/2 )
    
    def isSeatBFull(self):
        return ( self.seatB.__len__() == self.size/2 )
    
        
class Subject(models.Model):
    subID = models.CharField(max_length=20)
    subName = models.CharField(max_length=20) 
    examRoom =[]   

class Student(models.Model):
    stdID = models.CharField(max_length=20)
    stdName = models.CharField(max_length=50)
    examSub = []
    
