# al crear o actualizar una tarea, crear un log de la acción
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Task, logTask

@receiver(post_save, sender=Task)
def create_log_on_save(sender, instance, created, **kwargs):
    # Evitar log de actualización si es un "borrado lógico y manejarlo en el destroy del ViewSet"
    if not created and getattr(instance, 'is_deleted', False):
        return

    action = 'CREATED' if created else 'UPDATED'
    logTask.objects.create(task=instance, action=action)


