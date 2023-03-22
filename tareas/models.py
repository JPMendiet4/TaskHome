from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=180, blank=True, null=True)
    email = models.EmailField(max_length=150, blank=True, null=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
class Homework(models.Model):
    title = models.CharField(max_length=150, null=True)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    time = models.TimeField()
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title