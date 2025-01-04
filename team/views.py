import json

from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Team, Task, FriendRequest


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        user = request.user
        teams = Team.objects.filter(members=user)
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

def search(request):
    if request.method == "POST":
        search_term = request.POST['search_term']
        try:
            user = User.objects.get(username=search_term)
            return HttpResponseRedirect(reverse("profile", args=[search_term]))
        except User.DoesNotExist:
            teams = Team.objects.filter(members=request.user)
            return render(request,"index.html",{
                "teams":teams,
                "message": "No User with that username was found."
            })

def create_team(request):
    if request.method == 'POST':
        user=User.objects.get(username=request.user.username)
        team_name = request.POST['team_name']
        friends = request.POST.getlist('friends')
        team_description = request.POST['project_description']
        members= [user]
        for friend in friends:
            members.append(User.objects.get(username=friend))
        try:
            team = Team.objects.create(name=team_name,creator=user,description=team_description)
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

def team(request,team_name):
    team = Team.objects.get(name=team_name)
    user = User.objects.get(username=request.user)
    friends = user.friends.exclude(username=user.username)
    tasks = []

    for task in Task.objects.filter(team=team, completed=False):
        tasks.append(task)
    for task in Task.objects.filter(team=team, completed=True):
        tasks.append(task)

    return render(request, "team.html",
                  {"team": team, "friends": friends, "tasks": tasks, "members": team.members.all()})


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
        return HttpResponseRedirect(reverse("edit_members",args=[team_name,]))

@csrf_exempt
def profile(request,username):
        user = User.objects.get(username=username)
        if(request.user==user):
            friend_requests = FriendRequest.objects.filter(receiver=user)
            return render(request,"profile.html",{"profile_user":user,"friend_requests":friend_requests})

        try:
            friend_request_received=FriendRequest.objects.get(sender=user,receiver=request.user)
        except FriendRequest.DoesNotExist:
            friend_request_received = None
        try:
            friend_request_sent = FriendRequest.objects.get(receiver=user,sender=request.user)
        except FriendRequest.DoesNotExist:
            friend_request_sent = None

        return render(request,"profile.html",{"profile_user":user,"friend_request_received":friend_request_received,"friend_request_sent":friend_request_sent})

def friend_request(request,username):
    receiver=User.objects.get(username=username)
    friend_request = FriendRequest.objects.create(sender=request.user,receiver=receiver)
    friend_request.save()
    return HttpResponseRedirect(reverse("profile",args=[username]))

@csrf_exempt
def decline_friend_request(request,username):
    sender=User.objects.get(username=username)
    friend_request=FriendRequest.objects.get(sender=sender,receiver=request.user)
    friend_request.delete()
    return HttpResponseRedirect(reverse("profile",args=[username]))

@csrf_exempt
def accept_friend_request(request,username):
    sender = User.objects.get(username=username)
    friend_request = FriendRequest.objects.get(sender=sender,receiver=request.user)
    if friend_request:
        sender.friends.add(request.user)
        request.user.friends.add(sender)
        friend_request.delete()
    return HttpResponseRedirect(reverse("profile", args=[username]))

@csrf_exempt
def accept_friend_request_from_requests(request,username):
    sender = User.objects.get(username=username)
    friend_request = FriendRequest.objects.get(sender=sender,receiver=request.user)
    if friend_request:
        sender.friends.add(request.user)
        request.user.friends.add(sender)
        friend_request.delete()
    return JsonResponse({"message":"friend request accepted"})

def remove_friend_request(request,username):
    receiver = User.objects.get(username=username)
    friend_request = FriendRequest.objects.get(sender=request.user,receiver=receiver)
    friend_request.delete()
    return HttpResponseRedirect(reverse("profile",args=[username]))

def remove_friend(request,username):
    user=User.objects.get(username=username)
    user.friends.remove(request.user)
    user.save()
    return HttpResponseRedirect(reverse("profile",args=[username]))

@csrf_exempt
def edit_profile(request,feature_changed):
    user = User.objects.get(username=request.user.username)
    data = json.loads(request.body)
    print(data)
    if feature_changed == "username":
        try:
            user.username = data.get("body")
            user.save()
            return JsonResponse({"message":"User updated."})

        except IntegrityError:
            return JsonResponse({"message":"User does not exist."}, status=400)
    elif feature_changed == "bio":
        user.bio = data.get("body")
        user.save()
        return JsonResponse({"message":"User updated."})
    else:
        return JsonResponse({"message":"Invalid feature change"})

def report_progress(request,task):
    if request.method == 'POST':
         pass
    else:
        task =Task.objects.get(name=task)
        return render(request,"task.html",{"task":task})