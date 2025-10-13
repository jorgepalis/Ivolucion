Ivolucion
=================

API REST construida con Django 4.2 y Django REST Framework para autenticar usuarios mediante JWT, administrar Tareas y permisos administrados para estas.

Requisitos previos
------------------

- Python 3.12 (o compatible con el virtualenv incluido).
- Pip.

Configuración rápida con docker
--------------------

```bash
# levantar proyecto
docker-compose up

# en caso de hacer un cambio
docker-compose up --build
```

El servidor queda disponible en `http://127.0.0.1:8000/`. La documentación interactiva generada con drf-spectacular se expone en:

- `http://127.0.0.1:8000/api/swagger/`
- `http://127.0.0.1:8000/api/redoc/`
- Esquema OpenAPI: `http://127.0.0.1:8000/api/schema/`

Configuración rápida sin docker
--------------------

```bash
# crear y activar entorno si aún no existe
python -m venv env
env\Scripts\activate

# instalar dependencias
pip install -r requirements.txt

# aplicar migraciones y crear superusuario opcional
python manage.py migrate
python manage.py createsuperuser

# ejecutar el servidor
python manage.py runserver
```

El servidor queda disponible en `http://127.0.0.1:8000/`. La documentación interactiva generada con drf-spectacular se expone en:

- `http://127.0.0.1:8000/api/swagger/`
- `http://127.0.0.1:8000/api/redoc/`
- Esquema OpenAPI: `http://127.0.0.1:8000/api/schema/`



Dependencias principales
------------------------

- `django`: marco principal.
- `djangorestframework`: serialización y vistas REST.
- `djangorestframework-simplejwt`: emisión y refresco de tokens JWT.
- `drf-spectacular`: generación del esquema OpenAPI y documentación.

Estructura de aplicaciones
--------------------------

- `core`: configuración global, integración de SimpleJWT y ruteo de la documentación y URLs principales.
- `users`: gestión de usuarios (registro, login con JWT, permisos y serializadores para el frontend). Expone endpoints como `/api/users/token/`, `/api/users/token/refresh/`, `/api/users/register/` y `/api/users/me/`.
- `tasks`: modelo y API para administrar tareas, estados (`Status`) y categorías (`Category`). Endpoints típicos disponibles son `/api/tasks/`, `/api/status/` y `/api/categories/`.
- `pytest`: Configuración y pruebas de logica de negocio.

Lógica relevante
----------------

- El modelo `Task` relaciona título, descripción, usuario, estado y categoría. Cada tarea guarda un `created_at` automático.
- `Status` y `Category` son modelos separados para facilitar reutilización y filtrado.
- Hay un modelo `logTask` que registra acciones sobre tareas (`CREATED`, `UPDATED`, `DELETED`).
- Hay una señal encargada de crear `logTask` automaticamente al crear y editar tareas.
- Al crear una tarea desde la API el estado se fuerza a `Pendiente` (esto se implementa en el serializer). Al editar una tarea sí es posible cambiar su `status` mediante el campo `status_id`.
- La autenticación se realiza por JWT usando `djangorestframework-simplejwt`; muchas rutas requieren que el usuario esté autenticado.
- Cada app tiene una carpeta management con algunos comandos utiles para crear registros basicos de funcionamiento en la bd.
- Los usuarios con rol `client` pueden administrar sus propias tareas mientas que los usuarios de rol `admin` tienen control total.

Comandos útiles
---------------

```bash
# para crear roles en la bd
python manage.py create_roles

# para crear estados en la bd
python manage.py create_status


# para crear categorias en la bd
python manage.py create_categorys

```


Testing
---------------
```bash
# Para ejecutar los tests
python -m pytest
```

Usuarios de prueba
------------------

En la base de datos incluida puedes encontrar usuarios de prueba útiles para desarrollo. 

```bash
# Admin
Admin-user: admin@admin.com
Admin-password: Admin21. (incluido el punto)

# Cliente 1
Client-user1: user1@example.com
Client-password: Client21. (incluido el punto)

# Cliente 2
Client-user2: user2@example.com
Client-password: Client21. (incluido el punto)
```



Notas finales
------------

La API está pensada para integrarse con un frontend que use los endpoints protegidos mediante JWT. Revisa `core/settings.py` para configurar CORS, base de datos u otros ajustes de despliegue.
