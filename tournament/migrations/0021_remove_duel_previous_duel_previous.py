# Generated by Django 4.0.5 on 2022-06-19 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0020_duel_passed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='duel',
            name='previous',
        ),
        migrations.AddField(
            model_name='duel',
            name='previous',
            field=models.ManyToManyField(blank=True, to='tournament.duel'),
        ),
    ]
