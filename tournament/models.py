from faulthandler import disable
from tkinter import DISABLED
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Player(models.Model):
    """Player object that's related to Users in Django"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=150, null=True)

    def __str__(self):
        return str(self.name)
    
class Tournament(models.Model):
    """Tournament object that is related ForeignKey to owner,
    which means one owner can own many tournaments. 
    and ManyToMany with players who only play in it.
    Player invitation is initially skipped"""
    name = models.CharField(max_length=100)
    players = models.ManyToManyField(User, blank=True)
    max_players = models.PositiveSmallIntegerField(default=2)
    belongs_to = models.ForeignKey(User, related_name='creator', on_delete=models.CASCADE)
    start_date = models.DateTimeField('Starting on date')
    
    def __str__(self):
        return str(self.name)
# Create your models here.
