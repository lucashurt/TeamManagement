import json

from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.template.backends.utils import csrf_input
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Team, Task


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        user = request.user
        teams=[]
        for team in Team.objects.all():
            if team.members.filter(id=user.id).exists():
                teams.append(team)
        return render(request, 'index.html', {'teams':teams})
    else:
        return render(request, 'register.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password != confirm_password:
            return render(request, 'register.html', {
                "message": "Passwords must match."
            })
        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
        except IntegrityError:
            return render(request, 'register.html', {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, 'login.html', {
                "message": "Invalid username or password."
            })
    else:
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def create_team(request):
    if request.method == 'POST':
        user=User.objects.get(username=request.user.username)
        team_name = request.POST['team_name']
        friends = request.POST.getlist('friends')
        team_description = request.POST['project_description']
        team_deadline = request.POST['project_deadline']
        members= [user]
        for friend in friends:
            members.append(User.objects.get(username=friend))
        try:
            team = Team.objects.create(name=team_name,creator=user,description=team_description,deadline=team_deadline)
            team.members.set(members)
            team.admins.add(user)
            team.save()
        except IntegrityError:
            user = User.objects.get(username=request.user)
            friends = user.friends.exclude(username=user.username)
            return render(request, "create.html", {"message": "Team name already taken.", "friends":friends})
        return HttpResponseRedirect(reverse("index"))
    else:
        user = User.objects.get(username=request.user)
        friends = user.friends.exclude(username=user.username)
        return render(request, "create.html", {"friends":friends})

@csrf_exempt
def edit_members(request,team_name,):
    if request.method == 'POST':
        data=json.loads(request.body)
        team=Team.objects.get(name=team_name)
        if "remove" in data:
            try:
                user = User.objects.get(username=data["remove"])
                team.members.remove(user)
                team.save()
                return JsonResponse({"message":"User removed"})
            except User.DoesNotExist:
                return JsonResponse({"message": "User does not exist."}, status=400)
        elif "add" in data:
            try:
                user = User.objects.get(username=data["add"])
                team.members.add(user)
                team.save()
                return JsonResponse({"message":"User added"})
            except User.DoesNotExist:
                return JsonResponse({"message": "User does not exist."}, status=400)
    else:
        team = Team.objects.get(name=team_name)
        tasks = Task.objects.filter(team=team)
        user = User.objects.get(username=request.user)
        friends= user.friends.exclude(username=user.username)
        return render(request, "team.html", {"team":team, "friends":friends, "tasks":tasks,"members":team.members.all()})

def create_task(request,team_name):
    if request.method == 'POST':
        team=Team.objects.get(name=team_name)
        task_name = request.POST['task_name']
        task_description = request.POST['task_description']
        task_deadline = request.POST['task_deadline']
        task_priority = request.POST['task_priority']
        assigned_to = request.POST['assigned_to']
        user = User.objects.get(username=assigned_to)

        task=Task.objects.create(name=task_name,description=task_description,deadline=task_deadline,priority=task_priority,team=team,assigned_to=user)
        task.save()
        team.tasks.add(task)
        team.save()
        return HttpResponseRedirect(reverse("create_team"))