from django.db import models

# Create your models here.


class Laws(models.Model):
    country = models.CharField(max_length=30)
    law = models.TextField(max_length = 2000)

    def __str__(self):
        return self.country
class Score(models.Model):
    overall_score = models.IntegerField()
    read_score = models.FloatField()
    q1 = models.IntegerField()
    q2 = models.IntegerField()
    q3 = models.IntegerField()
    q4 = models.IntegerField()