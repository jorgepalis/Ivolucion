from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Task, Status, Category, logTask
from users.models import User
from .serializers import TaskSerializer, StatusSerializer, CategorySerializer, LogTaskSerializer
from users.permissions import IsAdmin, IsClient
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes


@extend_schema(tags=['Status'])
class StatusViewSet(viewsets.ModelViewSet):
    """ViewSet para manejar los estados de las tareas
     - solo los administradores pueden crear, actualizar y eliminar estados
     - los usuarios autenticados pueden ver los estados
    """
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
@extend_schema(tags=['Category'])
class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet para manejar las categorías de las tareas
     - solo los administradores pueden crear, actualizar y eliminar categorías
     - los usuarios autenticados pueden ver las categorías
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
@extend_schema(
    tags=['Task'],
    parameters=[
        OpenApiParameter(
            name='status',
            description='Filtra las tareas por el ID del estado',
            required=False,
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name='category',
            description='Filtra las tareas por el ID de la categoría',
            required=False,
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
        ),
    ],
)
class TaskViewSet(viewsets.ModelViewSet):
    """ViewSet para manejar las tareas
     - los administradores pueden ver, crear, actualizar y eliminar todas las tareas
     - los clientes pueden ver, crear, actualizar y eliminar solo sus propias tareas
     - la eliminación de una tarea es un "borrado lógico"
     - Filtrado por estado y categoría mediante query params: ?status=<status_id>&category=<category_id>
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsClient | IsAdmin]

    def get_queryset(self):
        user = self.request.user

        # base inicial: todo, ordenado por fecha de creación descendente
        queryset = Task.objects.all().order_by('-created_at')

        # si no es admin, mostrar solo las suyas que no estén borradas
        if not user.is_admin:
            queryset = queryset.filter(user=user, is_deleted=False)

        # aplicar filtros opcionales
        status_id = self.request.query_params.get('status')
        category_id = self.request.query_params.get('category')

        if status_id:
            queryset = queryset.filter(status_id=status_id)
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset

    def perform_create(self, serializer):
        # todas las tareas creadas se asignan al usuario autenticado y estado pendiente
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        # realizar un "borrado lógico"
        instance.is_deleted = True
        instance.save()
        # crear un log de la acción de borrado
        logTask.objects.create(task=instance, action='DELETED')


@extend_schema(tags=['LogTask'])
class LogTaskViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para manejar los logs de las tareas
     - solo los administradores pueden ver los logs
    """
    queryset = logTask.objects.all()
    serializer_class = LogTaskSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        return logTask.objects.all().order_by('-timestamp')
    

