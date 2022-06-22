from django.urls import path
from . import views

app_name = "main"   


urlpatterns = [
    path("", views.login_request, name="index"),
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
    path('<int:tournament_id>/generate', views.generate_duels, name="generate_duels"),
    path('<int:tournament_id>/<int:duel_id>/<int:user_id>/set_winner', views.set_duel_winner, name="set_duel_winner"),
    path('<int:tournament_id>/<int:round_to_be_updated>/update_round', views.update_round, name="update_round"),
]