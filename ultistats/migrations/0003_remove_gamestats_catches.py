# Generated by Django 5.1.3 on 2024-11-23 00:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ultistats', '0002_delete_season'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamestats',
            name='catches',
        ),
    ]
