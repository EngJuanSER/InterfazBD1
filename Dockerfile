# Dockerfile para Django + Oracle Client
FROM python:3.11-slim

# Establecer variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Instalar dependencias del sistema necesarias para Oracle Instant Client
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libaio1t64 \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Descargar e instalar Oracle Instant Client 21c (más estable)
RUN mkdir -p /opt/oracle && \
    cd /opt/oracle && \
    wget https://download.oracle.com/otn_software/linux/instantclient/2110000/instantclient-basic-linux.x64-21.10.0.0.0dbru.zip && \
    unzip instantclient-basic-linux.x64-21.10.0.0.0dbru.zip && \
    rm instantclient-basic-linux.x64-21.10.0.0.0dbru.zip && \
    cd instantclient_21_10 && \
    echo /opt/oracle/instantclient_21_10 > /etc/ld.so.conf.d/oracle-instantclient.conf && \
    ldconfig

# Establecer variables de entorno para Oracle
ENV LD_LIBRARY_PATH=/opt/oracle/instantclient_21_10:$LD_LIBRARY_PATH
ENV PATH=/opt/oracle/instantclient_21_10:$PATH

# Copiar requirements.txt
COPY requirements.txt /app/

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto
COPY . /app/

# Asegurar que entrypoint.sh tenga el formato correcto y permisos de ejecución
RUN chmod +x /app/entrypoint.sh && \
    sed -i 's/\r$//' /app/entrypoint.sh

# Exponer el puerto 8000
EXPOSE 8000

# Script de inicio
ENTRYPOINT ["/app/entrypoint.sh"]
