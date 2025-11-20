#!/bin/bash
# Script de inicio para el contenedor Django

echo "Esperando a que Oracle Database esté listo..."

# Esperar hasta que Oracle esté disponible
while ! nc -z oracle-db 1521; do
  sleep 1
done

echo "✓ Oracle Database está listo!"

# Ejecutar migraciones
echo "Ejecutando migraciones de Django..."
python manage.py migrate --noinput

# Iniciar servidor Django
echo "Iniciando servidor Django en 0.0.0.0:8000"
python manage.py runserver 0.0.0.0:8000
