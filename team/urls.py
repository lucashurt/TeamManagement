from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('create_team', views.create_team, name='create_team'),
    path('edit_members/<int:team_id>', views.edit_members, name='edit_team'),
]