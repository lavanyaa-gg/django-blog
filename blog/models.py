from django.db import models

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    favourite = models.BooleanField(default=False)
    vote = models.IntegerField(default=0)