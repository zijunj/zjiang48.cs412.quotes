# Generated by Django 5.1.3 on 2024-12-08 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ultistats', '0005_game_tournament'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='losses',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='team',
            name='rank',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='team',
            name='wins',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
