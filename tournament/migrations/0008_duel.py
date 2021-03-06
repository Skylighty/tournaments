# Generated by Django 4.0.5 on 2022-06-17 19:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tournament', '0007_alter_tournament_max_players'),
    ]

    operations = [
        migrations.CreateModel(
            name='Duel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player1', models.CharField(blank=True, max_length=100)),
                ('player2', models.CharField(blank=True, max_length=100)),
                ('players', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('tournament', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tournament.tournament')),
                ('winner', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='winner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
