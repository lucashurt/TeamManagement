from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('create_team', views.create_team, name='create_team'),
    path('create_task/<str:team_name>', views.create_task, name='create_task'),
    path('edit_members/<str:team_name>', views.edit_members, name='edit_team'),
]