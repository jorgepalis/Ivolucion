from tasks.models import Category
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Crea las categorías iniciales: trabajo, personal y otros'

    def handle(self, *args, **kwargs):
        categories = ['trabajo', 'personal', 'otros']
        for category_name in categories:
            category, created = Category.objects.get_or_create(name=category_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Categoría "{category_name}" creada exitosamente.'))
            else:
                self.stdout.write(f'La categoría "{category_name}" ya existe.')

        self.stdout.write(self.style.SUCCESS('Categorías iniciales creadas o ya existentes.'))