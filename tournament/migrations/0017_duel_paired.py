# Generated by Django 4.0.5 on 2022-06-19 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0016_duel_previous'),
    ]

    operations = [
        migrations.AddField(
            model_name='duel',
            name='paired',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pair', to='tournament.duel'),
        ),
    ]
