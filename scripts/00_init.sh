#!/bin/bash
# Script de inicialización para ejecutar los scripts SQL como usuario abogado

echo "Ejecutando scripts SQL como usuario abogado..."

# Esperar a que la base de datos esté lista
sleep 10

# Ejecutar el script de esquema
sqlplus -s abogado/abogado123@FREEPDB1 @/container-entrypoint-initdb.d/01_modelo.sql

# Ejecutar el script de datos
sqlplus -s abogado/abogado123@FREEPDB1 @/container-entrypoint-initdb.d/02_data.sql

echo "Scripts SQL ejecutados correctamente."
