# Generated by Django 5.1.1 on 2024-10-21 00:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mini_fb', '0003_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='message',
            new_name='image',
        ),
    ]
