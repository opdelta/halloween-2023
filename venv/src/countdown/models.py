from django.db import models

class Countdown(models.Model):
    target_date = models.DateTimeField()

class Message(models.Model):
    message = models.CharField(max_length=1000)
    api_endpoint_id = models.IntegerField(default=0) # 0 = no endpoint, 1 = add_time, 2 = remove_time, 3 = reset_target_date
    api_param_nb = models.IntegerField(default=0)
    been_seen = models.BooleanField(default=False)