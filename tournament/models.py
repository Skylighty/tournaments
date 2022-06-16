from django.db import models
from django.contrib.auth.models import User

class Player(models.Model):
    """Player object that's related to Users in Django"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=150, null=True)

    def __str__(self):
        return str(self.name)
    
class Tournament(models.Model):
    """Tournament object that is related OneToOne to owner, 
    and ManyToMany with players who only play in it"""
    belongs_to = models.OneToOneField(User, on_delete=models.CASCADE)
    players = models.ManyToManyField(Player)
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField('Date created')
    
    def __str__(self):
        return str(self.name)
# Create your models here.
