from math import log2
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from tournament.models import Tournament, Duel
from .forms import EditTournamentForm, NewUserForm, TournamentForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


# ================== USER RELATED =======================
def register_request(request):
    """Handle the registration request
    render empty form if no POST"""
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("/manage")
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
                return redirect("/manage")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="tournament/login.html", context={"login_form":form})


@login_required
def logout_request(request):
    """Handle the user logout request"""
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('/login')

# ===========================================================


# ================== TOURNAMENT RELATED =======================
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
                return redirect("/manage")
            else:
                messages.error(request,"Wrong data!")
                messages.error(request,str(form.errors))
    user = get_object_or_404(User, pk=request.user.id)
    form = TournamentForm(initial={
                "belongs_to":user,
                "start_date": timezone.now(),
                "started": False,
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
        return redirect("/manage")
    else:
        messages.error(request, "This is not your tournament!")
        return render(request=request, template_name="tournament/manage.html")


# RANDOM ELEMENT! MyModel.objects.order_by('?').first()
@login_required
def generate_duels(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    player_count = len(list(tournament.players.all()))
    tournament.started = True
    if request.user.is_authenticated:
        if player_count == tournament.max_players:
        # ---- INITIALIZE ------
            if Duel.objects.filter(tournament=tournament).exists() == False:
                # Convert QuerySet to list, so query doesn't db-level sort
                # everytime it's accessed
                random_players = list(tournament.players.order_by('?'))
                starting_duels_no = int(tournament.max_players/2)
                # Initialize random and unique starting duels 
                for i in range(0, (2*starting_duels_no), 2):
                    temp = Duel.objects.create(tournament=tournament,
                        player1=random_players[i],
                        player2=random_players[i+1],
                        max_rounds=starting_duels_no,
                        passed=False,
                        round=int(1))
                    temp.save()
                    temp.players.add(random_players[i],random_players[i+1])
                    temp.save()
                duels = list(Duel.objects.filter(tournament=tournament))
                if len(list(tournament.players.all())) <= tournament.rounds:
                    for i in range(len(duels)):
                        if i % 2 == 0:
                            duels[i].paired = duels[i+1]
                            duels[i+1].paired = duels[i]
                            duels[i].save()
                            duels[i+1].save()
                tournament.rounds = log2(tournament.max_players)
                tournament.current_round = 1
                tournament.save()
            else:
                if (Duel.objects.filter(tournament=tournament, round=tournament.current_round).filter(winner=None).exists() == False
                    and Duel.objects.filter(tournament=tournament, round=tournament.current_round).exists() == True
                    and Duel.objects.filter(tournament=tournament, round=tournament.current_round+1).exists() == False):
                    if (tournament.current_round != tournament.rounds and tournament.rounds != 1):
                        return redirect(f'/{tournament.id}/{tournament.current_round+1}/update_round')
                    else:
                        pass
                # else:
                #     continue
            
            duels = Duel.objects.filter(tournament=tournament)
            # TODO - iterative viewing on rounds
            #if Duel.objects.filter(tournament=tournament, round=1):
            context = {
                "tournament": tournament,
                "duels": duels,
            }
            return render(request=request, template_name='tournament/tournament_view.html', context=context)
        else:
            messages.error(request, f'You can\'t start tournament \'{tournament.name}\' - not all players are assigned to it!')
            return redirect("/manage")
    else:
        try:
            return render(request=request, template_name='tournament/tournament_view.html', context=context)
        except:
            messages.error("Sorry, You are not logged in!")


def anon_view(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    duels = Duel.objects.filter(tournament=tournament)
    context = {
        "tournament": tournament,
        "duels": duels,
    }
    return render(request=request, template_name='tournament/tournament_view.html', context=context)


@login_required
def update_round(request, tournament_id, round_to_be_updated):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    tournament.current_round = round_to_be_updated
    tournament.save()
    duels = list(Duel.objects.filter(tournament=tournament, round=round_to_be_updated-1))
    #next_round_duels_no = len(duels)/2
    #for i in range(next_round_duels_no):
    for duel in duels:
        if duel.passed is False and duel.paired.passed is False:
            new_duel = Duel.objects.create(tournament=tournament,
            player1=duel.winner,
            player2=duel.paired.winner,
            round=round_to_be_updated,
            passed=False)
            duel.passed = True
            duel.paired.passed = True
            new_duel.save()
            duel.save()
            duel.paired.save()
            new_duel.players.add(duel.winner)
            new_duel.players.add(duel.paired.winner)
            new_duel.previous.add(duel)
            new_duel.previous.add(duel.paired)
            new_duel.save()
    duels = list(Duel.objects.filter(tournament=tournament, round=round_to_be_updated))
    # Pairing duels for further updates
    for i in range(len(duels)):
        if i % 2 == 0 and len(duels) > 1:
                duels[i].paired = duels[i+1]
                duels[i+1].paired = duels[i]
                duels[i].save()
                duels[i+1].save()
    return redirect(f'/{tournament.id}/generate')


@login_required
def set_duel_winner(request, tournament_id, duel_id, user_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    duel = get_object_or_404(Duel, pk=duel_id)
    if not duel.winner:
        duel.winner = get_object_or_404(User, pk=user_id)
        duel.save()
    duels = list(Duel.objects.filter(tournament=tournament, round=duel.round))
    if len(duels) == 1:
        tournament.champion = duel.winner
        tournament.save()
    return redirect(f'/{tournament_id}/generate')
        

@login_required
def edit_tournament(request,tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    tournament.players.clear()
    if tournament.started is False:
        q2 = User.objects.all()
        if request.method == "POST":
            if request.user.is_authenticated:
                form = EditTournamentForm(request.POST, instance=tournament)
                if form.is_valid():
                    form.save()
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
                    "belongs_to": getattr(tournament, "belongs_to"),
                    "name": getattr(tournament, "name"),
                    "players": tournament.players.all()
                    })
        context = {
            "tournament": tournament,
            "users": q2,
            "edit_form": form,
        }
        return render(request=request, template_name="tournament/edit.html", context=context)
    else:
        messages.error(request, f'You cannot edit {tournament.name}. It has already begun!')
        return redirect('/manage')


@login_required
def manage_players(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    if tournament.started is False: 
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
                return redirect(f'/{tournament_id}/players')
        if request.method == "POST" and "remove" in request.POST:
            if request.user.is_authenticated:
                added_user_id = request.POST.get("user")
                tournament.players.remove(get_object_or_404(User, pk=added_user_id))
                tournament.save()
                messages.success(request, f"User {get_object_or_404(User,pk=added_user_id).username} removed from tournament {tournament.name}!")
                #return redirect(request, f"{tid}/add_player")     
            else:
                messages.error(request, "User not authenticated!")
                return redirect(f'/{tournament_id}/players')
        context = {
            "tournament": tournament,
            "users": users,
            "players": players,
        }
        return render(request=request, template_name="tournament/manage_players.html", context=context)
    else:
        messages.error(request, f'You cannot edit {tournament.name}. It has already begun!')
        return redirect('/manage')


def index(request):
    return render(request, "tournament/login.html")
# Create your views here.
