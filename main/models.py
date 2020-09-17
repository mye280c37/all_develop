from accounts.models import *
from django.db import models

# Create your models here.


class Plan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start = models.CharField(max_length=15)
    end = models.CharField(max_length=15)

    def __str__(self):
        return "[예정] "+self.user.username + " : " + str(self.date)


class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start = models.CharField(max_length=15)
    end = models.CharField(max_length=15)
    hours = models.IntegerField()
    contents = models.TextField()

    def __str__(self):
        return "[보고] "+self.user.username + " : " + str(self.date)
