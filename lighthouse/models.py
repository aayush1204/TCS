from django.db import models

# Create your models here.


class Laws(models.Model):
    country = models.CharField(max_length=30)
    law = models.TextField(max_length = 800)

