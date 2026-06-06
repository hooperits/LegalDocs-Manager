import logging
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Document

logger = logging.getLogger(__name__)


@receiver(post_delete, sender=Document)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem/storage when corresponding Document object is deleted.
    """
    if instance.file:
        try:
            instance.file.delete(save=False)
        except Exception as e:
            # Log the error but don't prevent database record deletion
            logger.error(f"Error deleting file {instance.file.name} from storage: {e}")


@receiver(pre_save, sender=Document)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem/storage when corresponding Document object
    is updated with a new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Document.objects.get(pk=instance.pk).file
    except Document.DoesNotExist:
        return False

    new_file = instance.file
    if old_file and old_file != new_file:
        try:
            old_file.delete(save=False)
        except Exception as e:
            logger.error(f"Error deleting old file {old_file.name} from storage: {e}")
