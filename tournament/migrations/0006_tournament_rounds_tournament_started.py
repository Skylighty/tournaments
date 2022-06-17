# Generated by Django 4.0.5 on 2022-06-17 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0005_tournament_max_players_alter_tournament_players'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='rounds',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='tournament',
            name='started',
            field=models.BooleanField(default=False, verbose_name='started'),
        ),
    ]
