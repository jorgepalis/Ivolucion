import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from users.models import Role
from tasks.models import Task, Status, Category


@pytest.fixture
def roles(db):
    # Crear roles necesarios para las pruebas
    admin_role = Role.objects.create(name="admin")
    client_role = Role.objects.create(name="client")
    return {"admin": admin_role, "client": client_role}


@pytest.fixture
def admin_user(db, roles):
    # Crear un usuario admin para las pruebas
    user_model = get_user_model()
    email = "admin@example.com"
    return user_model.objects.create_user(  # type: ignore[arg-type]
        email=email,
        password="adminpass123",
        role=roles["admin"],
        is_staff=True,
    )


@pytest.fixture
def client_user_a(db, roles):
    # Crear un usuario cliente para las pruebas
    user_model = get_user_model()
    email = "client_a@example.com"
    return user_model.objects.create_user(  # type: ignore[arg-type]
        email=email,
        password="clientpass123",
        role=roles["client"],
    )

@pytest.fixture
def client_user_b(db, roles):
    # Crear otro usuario cliente para las pruebas
    user_model = get_user_model()
    email = "client_b@example.com"
    return user_model.objects.create_user(  # type: ignore[arg-type]
        email=email,
        password="clientpass123",
        role=roles["client"],
    )

@pytest.fixture
def statuses(db):
    # Crear estados necesarios para las pruebas
    pending = Status.objects.create(name="pendiente")
    in_progress = Status.objects.create(name="en_progreso")
    completed = Status.objects.create(name="completado")
    return {"pendiente": pending, "en_progreso": in_progress, "completado": completed}

@pytest.fixture
def categories(db):
    # Crear categorías necesarias para las pruebas
    trabajo = Category.objects.create(name="trabajo")
    personal = Category.objects.create(name="personal")
    otro = Category.objects.create(name="otro")
    return {"trabajo": trabajo, "personal": personal, "otro": otro}

@pytest.fixture
def tasks(db, client_user_a, client_user_b, statuses, categories):
    # Crear tareas para los usuarios cliente
    task1 = Task.objects.create(
        title="Tarea 1",
        description="Descripción de la tarea 1",
        user=client_user_a,
        status=statuses["pendiente"],
        category=categories["trabajo"],
    )
    task2 = Task.objects.create(
        title="Tarea 2",
        description="Descripción de la tarea 2",
        user=client_user_a,
        status=statuses["en_progreso"],
        category=categories["personal"],
    )
    task3 = Task.objects.create(
        title="Tarea 3",
        description="Descripción de la tarea 3",
        user=client_user_b,
        status=statuses["completado"],
        category=categories["otro"],
    )
    return {"task1": task1, "task2": task2, "task3": task3}

@pytest.fixture
def api_client():
    # Proporcionar un cliente API para las pruebas
    return APIClient()

# solo usuarios admin pueden crear y editar estados.
@pytest.mark.django_db
class TestStatusWritePermissions:
    endpoint = "/api/status/"

    def test_only_admin_can_create_status(self, api_client, admin_user, client_user_a):
        # Intentar crear un estado como usuario cliente (debería fallar)
        api_client.force_authenticate(user=client_user_a)
        response = api_client.post(self.endpoint, {"name": "nuevo_estado"})
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # Crear un estado como usuario admin (debería tener éxito)
        api_client.force_authenticate(user=admin_user)
        response = api_client.post(self.endpoint, {"name": "nuevo_estado"})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "nuevo_estado"

    def test_only_admin_can_update_status(self, api_client, admin_user, client_user_a, statuses):
        status_id = statuses["pendiente"].id

        # Intentar actualizar un estado como usuario cliente (debería fallar)
        api_client.force_authenticate(user=client_user_a)
        response = api_client.put(f"{self.endpoint}{status_id}/", {"name": "estado_actualizado"})
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # Actualizar un estado como usuario admin (debería tener éxito)
        api_client.force_authenticate(user=admin_user)
        response = api_client.put(f"{self.endpoint}{status_id}/", {"name": "estado_actualizado"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "estado_actualizado"

# solo usuarios admin pueden crear y editar categorías.
@pytest.mark.django_db
class TestCategoryWritePermissions:
    endpoint = "/api/categories/"

    def test_only_admin_can_create_category(self, api_client, admin_user, client_user_a):
        # Intentar crear una categoría como usuario cliente (debería fallar)
        api_client.force_authenticate(user=client_user_a)
        response = api_client.post(self.endpoint, {"name": "nueva_categoria"})
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # Crear una categoría como usuario admin (debería tener éxito)
        api_client.force_authenticate(user=admin_user)
        response = api_client.post(self.endpoint, {"name": "nueva_categoria"})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "nueva_categoria"

    def test_only_admin_can_update_category(self, api_client, admin_user, client_user_a, categories):
        category_id = categories["trabajo"].id

        # Intentar actualizar una categoría como usuario cliente (debería fallar)
        api_client.force_authenticate(user=client_user_a)
        response = api_client.put(f"{self.endpoint}{category_id}/", {"name": "categoria_actualizada"})
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # Actualizar una categoría como usuario admin (debería tener éxito)
        api_client.force_authenticate(user=admin_user)
        response = api_client.put(f"{self.endpoint}{category_id}/", {"name": "categoria_actualizada"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "categoria_actualizada"

# usuarios autenticados pueden ver la lista de categorías.
@pytest.mark.django_db
class TestCategoryAccessPermissions:
    endpoint = "/api/categories/"

    def test_authenticated_user_can_view_categories(self, api_client, admin_user, client_user_a, categories):
        # Verificar que los usuarios autenticados pueden ver la lista de categorías
        api_client.force_authenticate(user=client_user_a)
        response = api_client.get(self.endpoint)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

        # verficar que los usuarios no autenticados no pueden ver la lista de categorías
        api_client.force_authenticate(user=None)
        response = api_client.get(self.endpoint)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

# usuarios autenticados pueden ver la lista de estados.
@pytest.mark.django_db
class TestStatusAccessPermissions:
    endpoint = "/api/status/"

    def test_authenticated_user_can_view_statuses(self, api_client, admin_user, client_user_a, statuses):
        # Verificar que los usuarios autenticados pueden ver la lista de estados
        api_client.force_authenticate(user=client_user_a)
        response = api_client.get(self.endpoint)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

        # verficar que los usuarios no autenticados no pueden ver la lista de estados
        api_client.force_authenticate(user=None)
        response = api_client.get(self.endpoint)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED



# usuarios admin pueden ver todas las tareas y usuarios clientes solo sus propias tareas.
@pytest.mark.django_db
class TestTaskAccessPermissions:
    endpoint = "/api/tasks/"

    def test_admin_can_view_all_tasks(self, api_client, admin_user, client_user_a, client_user_b, tasks):
        # Verificar que el usuario admin puede ver todas las tareas
        api_client.force_authenticate(user=admin_user)
        response = api_client.get(self.endpoint)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3  # Hay 3 tareas en total

    def test_client_can_view_own_tasks_only(self, api_client, client_user_a, client_user_b, tasks):
        # Verificar que el usuario cliente A puede ver solo sus propias tareas
        api_client.force_authenticate(user=client_user_a)
        response = api_client.get(self.endpoint)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2  # Cliente A tiene 2 tareas

        # Verificar que el usuario cliente B puede ver solo su propia tarea
        api_client.force_authenticate(user=client_user_b)
        response = api_client.get(self.endpoint)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1  # Cliente B tiene 1 tarea

    def test_unauthenticated_user_cannot_view_tasks(self, api_client):
        # Verificar que los usuarios no autenticados no pueden ver las tareas
        api_client.force_authenticate(user=None)
        response = api_client.get(self.endpoint)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


# pruebas de escritura de tareas
@pytest.mark.django_db
class TestTaskWritePermissions:
    endpoint = "/api/tasks/"

    def test_client_can_create_task(self, api_client, client_user_a, statuses, categories):
        # Verificar que el usuario cliente puede crear una tarea
        api_client.force_authenticate(user=client_user_a)
        response = api_client.post(self.endpoint, {
            "title": "Nueva Tarea",
            "description": "Descripción de la nueva tarea",
            "category_id": categories["trabajo"].id
        })
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == "Nueva Tarea"
        assert response.data["status"]["name"].lower() == "pendiente"  # El estado debe ser 'pendiente' por defecto

    def test_client_cannot_create_task_with_duplicate_title(self, api_client, client_user_a, tasks, categories):
        # Verificar que el usuario cliente no puede crear una tarea con un título duplicado
        api_client.force_authenticate(user=client_user_a)
        response = api_client.post(self.endpoint, {
            "title": "Tarea 1",  # Título duplicado
            "description": "Otra descripción",
            "category_id": categories["personal"].id,
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Ya existe una tarea con el mismo título para este usuario." in str(response.data)

    def test_unauthenticated_user_cannot_create_task(self, api_client, categories):
        # Verificar que los usuarios no autenticados no pueden crear tareas
        api_client.force_authenticate(user=None)
        response = api_client.post(self.endpoint, {
            "title": "Tarea Sin Autenticar",
            "description": "Descripción",
            "category_id": categories["otro"].id,
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_client_only_update_own_task(self, api_client, client_user_a, client_user_b, tasks, categories):
        task_id = tasks["task1"].id

        # Verificar que el usuario cliente A puede actualizar su propia tarea
        api_client.force_authenticate(user=client_user_a)
        response = api_client.put(f"{self.endpoint}{task_id}/", {
            "title": "Tarea 1 Actualizada",
            "description": "Descripción actualizada",
            "category_id": categories["personal"].id,
            "status_id": tasks["task1"].status.id,
        })
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Tarea 1 Actualizada"

        # Verificar que el usuario cliente B no puede actualizar la tarea del cliente A
        api_client.force_authenticate(user=client_user_b)
        response = api_client.put(f"{self.endpoint}{task_id}/", {
            "title": "Intento de Actualización",
            "description": "Descripción",
            "category_id": categories["otro"].id,
            "status_id": tasks["task1"].status.id,
        })
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_admin_can_update_any_task(self, api_client, admin_user, client_user_a, tasks, categories):
        task_id = tasks["task1"].id

        # Verificar que el usuario admin puede actualizar cualquier tarea
        api_client.force_authenticate(user=admin_user)
        response = api_client.put(f"{self.endpoint}{task_id}/", {
            "title": "Tarea 1 Actualizada por Admin",
            "description": "Descripción actualizada por admin",
            "category_id": categories["otro"].id,
            "status_id": tasks["task1"].status.id,
        })
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Tarea 1 Actualizada por Admin"
