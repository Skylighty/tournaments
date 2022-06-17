#from re import L
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from tournament.models import Tournament
from .forms import EditTournamentForm, NewUserForm, TournamentForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


def register_request(request):
    """Handle the registration request
    render empty form if no POST"""
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
    """Handle login requests
    render empty form if not POST"""
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


@login_required
def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('/index')


@login_required
def create_tournament(request):
    """Handle tournament creation,
    render pre-valued, but hidden option if no POST"""
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
    user = get_object_or_404(User, pk=request.user.id)
    form = TournamentForm(initial={
                "belongs_to":user,
                "start_date": timezone.now()
                })
    return render(request=request, template_name="tournament/create_tournament.html", context={"create_tournament_form":form})


@login_required
def manage_tournaments(request):
    """Handle redirection to tournament management"""
    #if request.user.is_authenticated:
    q1 = Tournament.objects.all()
    context = {
        "user_tournament_list": q1
    }
    return render(request=request, template_name="tournament/manage.html", context=context)
    # else:
    #     messages.error(request, "Only Users can manage their tournaments!")
    #     return redirect('/index')
    

def all_tournaments_view(request):
    q1 = Tournament.objects.all()
    context = {
        "all_tournaments": q1
    }
    return render(request=request, template_name="tournament/listview.html", context=context)


def tournament_view(request, tournament_id):
    q1 = Tournament.objects.filter(pk=tournament_id)
    context = {
        "tournament" : q1,
    }
    return render(request=request, template_name="tournament/tournament_view.html", context=context)


@login_required
def delete_tournament(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    temp_name = tournament.name
    if request.user.is_authenticated:
        tournament.delete()
        q1 = Tournament.objects.all()
        context = {
            "user_tournament_list": q1,
        }
        messages.success(request, f"Tournament: {temp_name} has been successfully deleted.")
        return render(request=request, template_name="tournament/manage.html", context=context)
    else:
        messages.error(request, "This is not your tournament!")
        return render(request=request, template_name="tournament/index.html")


@login_required
def edit_tournament(request,tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    tournament.players.clear()
    q2 = User.objects.all()
    if request.method == "POST":
        if request.user.is_authenticated:
            form = EditTournamentForm(request.POST)
            if form.is_valid():
                tournament = form.save(commit=False)
                tournament.save()
                form.save_m2m()
                print("zrobilemto")
                #form.save()
                messages.success(request, f'Tournament {form.cleaned_data.get("name")} has been saved successfully!')
                return redirect("/manage")
            else:
                messages.error(request, "Something is wrong!")
                messages.error(request,str(form.errors))
    #user = User.get_object_or_404(pk=request.user.id)
    print(getattr(tournament, "max_players"))
    form = EditTournamentForm(initial={
                "start_date": getattr(tournament, "start_date"),
                "max_players": getattr(tournament, "max_players"),
                "name": getattr(tournament, "name"),
                })
    context = {
        "tournament": tournament,
        "users": q2,
        "edit_form": form,
    }
    return render(request=request, template_name="tournament/edit.html", context=context)


@login_required
def manage_players(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    tid = str(tournament.id)
    users = User.objects.all()
    players = tournament.players.all()
    if request.method == "POST" and "add" in request.POST:
        if request.user.is_authenticated:
            added_user_id = request.POST.get("user")
            tournament.players.add(get_object_or_404(User, pk=added_user_id))
            tournament.save()
            messages.success(request, f"User {get_object_or_404(User,pk=added_user_id).username} sucessfully added to tournament {tournament.name}!")
            #return redirect(request, f"{tid}/add_player")     
        else:
            messages.error(request, "User not authenticated!")
            return redirect(request, 'tournament/index.html')
    if request.method == "POST" and "remove" in request.POST:
        if request.user.is_authenticated:
            added_user_id = request.POST.get("user")
            tournament.players.remove(get_object_or_404(User, pk=added_user_id))
            tournament.save()
            messages.success(request, f"User {get_object_or_404(User,pk=added_user_id).username} removed from tournament {tournament.name}!")
            #return redirect(request, f"{tid}/add_player")     
        else:
            messages.error(request, "User not authenticated!")
            return redirect(request, 'tournament/index.html')
    context = {
        "tournament": tournament,
        "users": users,
        "players": players,
    }
    return render(request=request, template_name="tournament/manage_players.html", context=context)


def index(request):
    return render(request, "tournament/index.html")
# Create your views here.
