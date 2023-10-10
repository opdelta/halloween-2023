from django.db import models

class Countdown(models.Model):
    target_date = models.DateTimeField()