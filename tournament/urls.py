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
]