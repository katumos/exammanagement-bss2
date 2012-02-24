from django.db import models

class AdminData(models.Model):
    UserName = models.CharField(max_length=70)
    Password = models.CharField(max_length=30)
    
    def __unicode__(self):
        return u' %s %s' % (self.UserName,self.Password)


