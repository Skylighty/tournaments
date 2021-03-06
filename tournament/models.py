from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Tournament(models.Model):
    """Tournament object that is related ForeignKey to owner,
    which means one owner can own many tournaments. 
    and ManyToMany with players who only play in it.
    Player invitation is initially skipped"""
    name = models.CharField(max_length=100)
    players = models.ManyToManyField(User, blank=True)
    max_players = models.IntegerField(default=2, validators=[MaxValueValidator(16), MinValueValidator(2)])
    belongs_to = models.ForeignKey(User, related_name='creator', on_delete=models.CASCADE)
    start_date = models.DateTimeField('Starting on date')
    started = models.BooleanField(verbose_name=('started'), default=False)
    rounds = models.IntegerField(default=0, blank=True)
    champion = models.ForeignKey(User, related_name='won_by', null=True, on_delete=models.CASCADE, blank=True)
    current_round = models.IntegerField(default=1)
    
    def __str__(self):
        return str(self.name)
# Create your models here.

class Duel(models.Model):
    """Data model of a duel between
    two players"""
    players = models.ManyToManyField(User, blank=True)
    winner = models.ForeignKey(User, related_name='winner', null=True,on_delete=models.CASCADE, blank=True)
    paired = models.ForeignKey('self', related_name='pair', null=True, on_delete=models.CASCADE, blank=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    player1 = models.ForeignKey(User, related_name='player1', on_delete=models.CASCADE, max_length=100, blank=True)
    player2 = models.ForeignKey(User, related_name='player2', on_delete=models.CASCADE, max_length=100, blank=True)
    previous = models.ManyToManyField('self', blank=True)
    max_rounds = models.IntegerField(default=1)
    passed = models.BooleanField(default=False)
    round = models.IntegerField(default=1)

