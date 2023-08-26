from django.db import models

# Create your models here.
class Wordgame(models.Model):
    word = models.CharField(max_length=100)
    
# Create your models here.
class ButtonPressed(models.Model):
    user = models.CharField(max_length=255)
    csrf = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.userid.username + " " + self.csrf + " " + str(self.time)