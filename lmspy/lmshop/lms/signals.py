from django.core.files.storage import default_storage
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from lms.models import Image
import os, glob


@receiver(pre_delete, sender=Image, dispatch_uid='question_delete_signal')
def log_deleted_question(sender, instance, using, **kwargs):
    for file in glob.glob(f"{default_storage.path(str(instance.image))}*"):
        os.remove(file)
