from rest_framework import serializers
from .models import Task, Status, Category, logTask
from users.serializers import UserDetailSerializer

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    status = StatusSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    status_id = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all(), source='status', write_only=True, required=False)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'user', 'status', 'category', 'is_deleted', 'created_at', 'status_id', 'category_id']
        read_only_fields = ['id', 'is_deleted', 'created_at']

    def create(self, validated_data):
        """fuerza el estado de la tarea a 'Pendiente' en la creación
         y valida que el usuario no tenga otra tarea con el mismo título.
        """
        validated_data.pop('status', None)

        # intentar encontrar el estado existente llamado 'pendiente' (insensible a mayúsculas)
        pending = Status.objects.filter(name__iexact='pendiente').first()
        if not pending:
            # devolver un error si no existe el estado pendiente
            raise serializers.ValidationError("El estado 'Pendiente' no existe. Por favor, creelo primero.")

        validated_data['status'] = pending

        #validar que el usuario no tenga una tarea con el mismo titulo
        user = self.context['request'].user
        if Task.objects.filter(user=user, title=validated_data['title']).exists():
            raise serializers.ValidationError("Ya existe una tarea con el mismo título para este usuario.")
        return super().create(validated_data)

class LogTaskSerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only=True)

    class Meta:
        model = logTask
        fields = ['id', 'task', 'action', 'timestamp']
        read_only_fields = ['id', 'timestamp']
