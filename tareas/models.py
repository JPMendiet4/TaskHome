from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=180, blank=True, null=True)
    email = models.EmailField(max_length=150, blank=True, null=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True)
    status = models.BooleanField(default=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Homework(models.Model):
    STATUS_CHOICES = (
        ('C', 'Creado'),
        ('P', 'En proceso'),
        ('T', 'Terminado'),
    )

    title = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    time = models.TimeField(blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='C')

    def __str__(self):
        return self.title

    def get_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status)