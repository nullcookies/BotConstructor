from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Bot


@receiver(post_delete, sender=Bot)
def submission_delete(sender, instance, **kwargs):
    instance.file_script.delete(False)
    instance.file_config.delete(False)
