# Generated by Django 3.2.18 on 2023-03-29 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tareas', '0004_auto_20230328_1258'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homework',
            name='status',
        ),
        migrations.RemoveField(
            model_name='user',
            name='delete_user',
        ),
        migrations.AddField(
            model_name='homework',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]