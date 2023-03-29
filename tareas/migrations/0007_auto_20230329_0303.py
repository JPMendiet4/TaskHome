# Generated by Django 3.2.18 on 2023-03-29 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tareas', '0006_user_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homework',
            name='active',
        ),
        migrations.AddField(
            model_name='homework',
            name='status',
            field=models.CharField(choices=[('C', 'Creado'), ('P', 'En proceso'), ('T', 'Terminado')], default='C', max_length=1),
        ),
    ]
