from django.db import models

# Create your models here.

class Note(models.Model):
    title = models.CharField(max_length=20)
    text = models.CharField(max_length=120)
    created = models.DateTimeField(auto_now_add=True)
    favourite = models.BooleanField(default=False)