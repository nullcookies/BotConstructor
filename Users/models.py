from django.db import models
from django.contrib.auth.models import User

from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='user_images/', blank=True,
        verbose_name='')
    about = models.CharField(max_length=500)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        if self.id and self.image:
            image = Image.open(self.image)
            width, height = image.size

            image = image.resize((width//2, height//2), Image.ANTIALIAS)
            image.save(self.image.path, optimize=True, quality=100)
        else:
            return
