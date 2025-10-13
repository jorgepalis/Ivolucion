from tasks.models import Status
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Crea los estados iniciales: pendiente, en_progreso y completada'

    def handle(self, *args, **kwargs):
        statuses = ['pendiente', 'cancelada', 'completada']
        for status_name in statuses:
            status, created = Status.objects.get_or_create(name=status_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Estado "{status_name}" creado exitosamente.'))
            else:
                self.stdout.write(f'El estado "{status_name}" ya existe.')

        self.stdout.write(self.style.SUCCESS('Estados iniciales creados o ya existentes.'))

            