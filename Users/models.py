from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default='media/default.png', upload_to='user_images/', blank=True)
    about = models.CharField(max_length=500)

    def __str__(self):
        return self.user.username
