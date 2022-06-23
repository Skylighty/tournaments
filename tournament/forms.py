from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from tournament.models import Tournament

# Create your forms here.
PLAYER_COUNT_CHOICES=[tuple([x,x]) for x in [2,4,8,16]]


class NewUserForm(UserCreationForm):
    """Usage of built-in register form"""
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class TournamentForm(forms.ModelForm):
    """Create tournament form basing on model"""
    class Meta:
        model = Tournament
        fields = ['name',
                  'players',
                  'max_players',
                  'belongs_to',
                  'start_date',
                  'started',
                  'rounds',
                  'champion',
                  'current_round']
        widgets = {
            'max_players': forms.Select(choices=PLAYER_COUNT_CHOICES),
            'belongs_to': forms.HiddenInput(),
            'started': forms.HiddenInput(),
            'rounds': forms.HiddenInput(),
            'players': forms.SelectMultiple(),
            'champion': forms.HiddenInput(),
            'current_round': forms.HiddenInput(),
        }
        
        
class EditTournamentForm(forms.ModelForm):
    """Edit tournament form basing on model"""
    class Meta:
        model = Tournament
        fields = ['name',
                  'players',
                  'max_players',
                  'belongs_to',
                  'start_date',
                  'started',
                  'rounds',
                  'champion',]
        widgets = {
            'max_players': forms.Select(choices=PLAYER_COUNT_CHOICES),
            'belongs_to': forms.HiddenInput(),
            'started': forms.HiddenInput(),
            'rounds': forms.HiddenInput(),
            'champion': forms.HiddenInput(),
            'current_round': forms.HiddenInput(),
        }

