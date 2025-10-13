from users.models import Role
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Crea los roles iniciales: admin y client'

    def handle(self, *args, **kwargs):
        roles = ['admin', 'client']
        for role_name in roles:
            role, created = Role.objects.get_or_create(name=role_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Rol "{role_name}" creado exitosamente.'))
            else:
                self.stdout.write(f'El rol "{role_name}" ya existe.')


            