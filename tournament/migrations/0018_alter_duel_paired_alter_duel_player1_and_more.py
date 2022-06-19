# Generated by Django 4.0.5 on 2022-06-19 13:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tournament', '0017_duel_paired'),
    ]

    operations = [
        migrations.AlterField(
            model_name='duel',
            name='paired',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pair', to='tournament.duel'),
        ),
        migrations.AlterField(
            model_name='duel',
            name='player1',
            field=models.ForeignKey(blank=True, max_length=100, on_delete=django.db.models.deletion.CASCADE, related_name='player1', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='duel',
            name='player2',
            field=models.ForeignKey(blank=True, max_length=100, on_delete=django.db.models.deletion.CASCADE, related_name='player2', to=settings.AUTH_USER_MODEL),
        ),
    ]