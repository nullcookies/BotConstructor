from django.db import models

from Users.models import Profile


class Bot(models.Model):
    file_script = models.FileField(upload_to='ScriptBots/')
    file_config = models.FileField(upload_to='ScriptBots/')
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True)
    access_token = models.CharField(max_length=200)
    title = models.CharField(max_length=50)
    username = models.CharField(max_length=50)

    def __str__(self):
        return self.access_token
