from django.db.models.signals import post_delete
from django.dispatch import receiver

from file_management.models import File


@receiver(post_delete, sender=File)
def post_delete_file(sender, instance, using, **kwargs):
    instance.file.delete(save=False)
