import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    friends = models.ManyToManyField('self', related_name='friends', blank=True)

class Task(models.Model):
    completed = models.BooleanField(default=False)
    assigned_to = models.ForeignKey('User', on_delete=models.CASCADE, related_name='assigned_tasks')
    deadline = models.DateTimeField()
    priority = models.IntegerField(default=0)
    progress = models.TextField()
    team=models.ForeignKey('Team', on_delete=models.CASCADE, related_name='tasks',default=None)

class Team(models.Model):
    name = models.CharField(max_length=50, unique=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teams_created',null=True)
    members = models.ManyToManyField('User', related_name='teams', blank=True)
    deadline = models.DateField(default=datetime.date.today)
    description = models.TextField(blank=True,default='')
    archived = models.BooleanField(default=False)
    admins = models.ManyToManyField('User', related_name='admins', blank=True)


