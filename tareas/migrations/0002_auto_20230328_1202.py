# Generated by Django 3.2.18 on 2023-03-28 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tareas', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='homework',
            old_name='active',
            new_name='delete',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='active',
            new_name='delete',
        ),
    ]
