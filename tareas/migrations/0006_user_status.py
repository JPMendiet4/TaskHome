# Generated by Django 3.2.18 on 2023-03-29 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tareas', '0005_auto_20230329_0236'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]