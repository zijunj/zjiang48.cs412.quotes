# Generated by Django 5.1.1 on 2024-10-21 00:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mini_fb', '0002_statusmessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateField(auto_now=True)),
                ('message', models.ImageField(blank=True, upload_to='')),
                ('StatusMessage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mini_fb.statusmessage')),
            ],
        ),
    ]