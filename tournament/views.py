#from re import L
from django.utils import timezone
from django.shortcuts import render, redirect
from tournament.models import Tournament
from .forms import NewUserForm, TournamentForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("/index")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="tournament/register.html", context={"register_form":form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/index")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="tournament/login.html", context={"login_form":form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('/index')

def create_tournament(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            form = TournamentForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,f"You've successfully created tournament: {form.cleaned_data.get('name')}!")
                return redirect("/index")
            else:
                messages.error(request,"Wrong data!")
                messages.error(request,str(form.errors))
    user = User.objects.get(pk=request.user.id)
    form = TournamentForm(initial={
                "belongs_to":user,
                "start_date": timezone.now()
                })
    return render(request=request, template_name="tournament/create_tournament.html", context={"create_tournament_form":form})



def index(request):
    return render(request, "tournament/index.html")
# Create your views here.
