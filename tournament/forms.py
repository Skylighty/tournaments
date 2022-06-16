from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from tournament.models import Tournament, Player

# Create your forms here.

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

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
    
    class Meta:
        model = Tournament
        fields = ['name',
                  'players',
                  'belongs_to',
                  'start_date',]
