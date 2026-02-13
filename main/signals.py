import logging

from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import IntakeFile

logger = logging.getLogger(__name__)


def _delete_file_from_storage(field_file):
    """Delete the backing object from the configured storage backend."""
    if not field_file:
        return

    file_name = getattr(field_file, "name", "")
    if not file_name:
        return

    try:
        field_file.storage.delete(file_name)
    except Exception:
        logger.exception("Failed to delete file from storage: %s", file_name)


@receiver(post_delete, sender=IntakeFile)
def delete_intake_file_blob_on_model_delete(sender, instance, **kwargs):
    """
    Remove uploaded blobs when IntakeFile rows are deleted.
    Works for local media and remote backends (e.g., S3) via Django storage API.
    """
    file_name = getattr(instance.file, "name", "")
    if not file_name:
        return

    # Guard against deleting a file path still referenced by another row.
    if sender.objects.filter(file=file_name).exists():
        return

    _delete_file_from_storage(instance.file)
