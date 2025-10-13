# Imagen base ligera con Python
FROM python:3.12-slim

# Evitar buffers de salida y establecer directorio
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Copiar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto
COPY . .

# Exponer el puerto de Django
EXPOSE 8000

# Comando por defecto
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
