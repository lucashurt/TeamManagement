from django.contrib import admin
from .models import User,Task,Team,FriendRequest
# Register your models here.

admin.site.register(User)
admin.site.register(Task)
admin.site.register(Team)
admin.site.register(FriendRequest)