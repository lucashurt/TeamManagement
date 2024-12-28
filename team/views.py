from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from team.models import User, Team


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        user = request.user
        teams=[]
        for team in Team.objects.all():
            if team.members.filter(id=user.id).exists():
                teams.append(team)
        return render(request, 'templates/index.html', {'teams':teams})
    else:
        return render(request, 'templates/register.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password != confirm_password:
            return render(request, 'templates/register.html', {
                "message": "Passwords must match."
            })
        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
        except IntegrityError:
            return render(request, 'templates/register.html', {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, 'templates/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, 'templates/login.html', {
                "message": "Invalid username or password."
            })
    else:
        return render(request, 'templates/login.html')

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
            return render(request, "templates/create.html", {"message": "Team name already taken.", "friends":friends})
        return HttpResponseRedirect(reverse("index"))
    else:
        user = User.objects.get(username=request.user)
        friends = user.friends.exclude(username=user.username)
        return render(request, "templates/create.html", {"friends":friends})

def edit_members(request, team_id):
    if request.method == 'POST':
        pass
    else:
        team = Team.objects.get(pk=team_id)
        user = User.objects.get(username=request.user)
        friends= user.friends.exclude(username=user.username)
        return render(request, "templates/team.html", {"team":team, "friends":friends, "members":team.members.all()})