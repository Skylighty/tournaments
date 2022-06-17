from django.urls import path
from . import views

app_name = "main"   


urlpatterns = [
    path("index", views.index, name="index"),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("create", views.create_tournament, name="create_tournament"),
    path("manage", views.manage_tournaments, name="manage"),
    path('listview', views.all_tournaments_view, name="all_tournaments"),
    path('<int:tournament_id>/view', views.tournament_view, name="tournament_view"),
    path('<int:tournament_id>/edit', views.edit_tournament, name="tournament_edit"),
    path('<int:tournament_id>/delete', views.delete_tournament, name="tournament_delete"),
    path('<int:tournament_id>/players', views.manage_players, name="manage_players"),
]