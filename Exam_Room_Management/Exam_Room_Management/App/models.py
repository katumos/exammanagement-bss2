from django.db import models

class Member(models.Model):
    username = models.CharField(max_length=22)
    password = models.IntegerField(max_length=22)

    def __unicode__(self):
    	return u' %s %s' % (self.username,self.password)


class ExamStudentSeat(models.Model):
    roomID = models.CharField(max_length=10)
    time = models.CharField(max_length=20)
    date = models.CharField(max_length=20)
    subj = models.CharField(max_length=20)
    seater = models.CharField(max_length=20)

class ExamRoomInfo(models.Model):
    roomID = models.CharField(max_length=10)
    time = models.CharField(max_length=20)
    date = models.CharField(max_length=20)
    subj = models.CharField(max_length=20)    
    capacity = models.IntegerField()
    size = models.IntegerField()
    
class ExamSubjectInfo(models.Model):
    subjID = models.CharField(max_length=20)
    subjName = models.CharField(max_length=20)
    
class ExamStudentInfo(models.Model):
    stdID = models.CharField(max_length=20)
    stdName = models.CharField(max_length=50)
    
