from django.db import models

class Exam_Room(models.Model):
    roomID = models.CharField(max_length=10)    
    subA_timeA = models.CharField(max_length=20)
    subA_timeB = models.CharField(max_length=20)
    subB_timeA = models.CharField(max_length=20)
    subB_timeB = models.CharField(max_length=20)
    timeA = models.CharField(max_length=20)
    timeB = models.CharField(max_length=20)
    size = models.IntegerField()
    seatA_timeA = []
    seatA_timeB = []
    seatB_timeA = []
    seatB_timeB = []    
    
    def isSeatATimeAFull(self):
        return (self.seatA_timeA.__len__() == self.size/2)
    
    def isSeatATimeBFull(self):
        return (self.seatA_timeA.__len__() == self.size/2)
    
    def isSeatBTimeAFull(self):
        return (self.seatB_timeA.__len__() == self.size/2)
    
    def isSeatBTimeBFull(self):
        return (self.seatB_timeA.__len__() == self.size/2)
      

class Subject(models.Model):
    subID = models.CharField(max_length=20)
    subName = models.CharField(max_length=20) 
    roomList = []
    stdList = []   

class Student(models.Model):
    stdID = models.CharField(max_length=20)
    stdName = models.CharField(max_length=50)
    examInfo = []
        
