from accounts.models import *
from django.db import models

# Create your models here.


class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    hours = models.IntegerField()
    contents = models.TextField()

    def __str__(self):
        return self.user.username + " : " + str(self.date)

