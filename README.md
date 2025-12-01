# Sistema de Gestion Legal - InterfazBD1

Sistema web de gestion de casos legales desarrollado con Django y Oracle Database. Este proyecto utiliza SQL Nativo (Raw SQL) en lugar del ORM de Django para cumplir con requisitos academicos.

## Caracteristicas Principales

- Registro y gestion de clientes
- Gestion de casos legales con especializaciones (Penal, Civil, Laboral, Administrativo)
- Gestion de expedientes con etapas procesales
- Manejo de sucesos, resultados y documentos por expediente
- Navegacion entre etapas e instancias
- Impresion de casos completos
- Carga de documentos PDF

## Tecnologias Utilizadas

- Python 3.11
- Django 5.2
- Oracle Database 21c XE
- Bootstrap 5
- Docker y Docker Compose

## Instalacion

Existen dos formas de ejecutar el proyecto:

### Opcion 1: Usando Docker (Recomendado)

Esta es la forma mas sencilla y no requiere instalar Oracle localmente.

#### Requisitos Previos

- Docker (version 20.10 o superior)
- Docker Compose (version 2.0 o superior)

#### Pasos de Instalacion

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd InterfazBD1
```

2. Crear archivo `.env` en la raiz del proyecto:
```bash
cp .env.example .env
```

Editar `.env` y configurar las variables:
```
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=localhost:1521/FREEPDB1
DB_USER=abogado
DB_PASSWORD=abogado123
```

3. Levantar los contenedores:
```bash
sudo docker compose up -d --build
```

4. Esperar 60 segundos para que Oracle inicialice completamente.

5. Acceder a la aplicacion:
```
http://localhost:8000/clientes/
```

#### Comandos Utiles con Docker

Detener los contenedores:
```bash
sudo docker compose down
```

Reiniciar desde cero (borra datos):
```bash
sudo docker compose down -v
sudo docker compose up -d --build
```

Ver logs en tiempo real:
```bash
sudo docker compose logs -f web
sudo docker compose logs -f oracle
```

### Opcion 2: Instalacion Local (Sin Docker)

Si prefieres ejecutar la aplicacion localmente sin Docker.

#### Requisitos Previos

- Python 3.11 o superior
- Oracle Database 21c XE instalado localmente
- Oracle Instant Client (para conexion desde Python)

#### Pasos de Instalacion

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd InterfazBD1
```

2. Crear y activar entorno virtual:

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar Oracle Database:

Conectarse a Oracle como SYSDBA y ejecutar:

**Linux/Mac:**
```bash
sqlplus sys/password@localhost:1521/FREEPDB1 as sysdba
```

**Windows:**
```cmd
sqlplus sys/password@localhost:1521/FREEPDB1 as sysdba
```

Luego ejecutar:
```sql
CREATE USER abogado IDENTIFIED BY abogado123;
GRANT CONNECT, RESOURCE TO abogado;
GRANT CREATE SESSION TO abogado;
GRANT UNLIMITED TABLESPACE TO abogado;
EXIT;
```

5. Ejecutar scripts de base de datos:

**Linux/Mac:**
```bash
sqlplus abogado/abogado123@localhost:1521/FREEPDB1
@scripts/01_modelo.sql
@scripts/02_data.sql
exit
```

**Windows:**
```cmd
sqlplus abogado/abogado123@localhost:1521/FREEPDB1
@scripts\01_modelo.sql
@scripts\02_data.sql
exit
```

6. Crear archivo `.env` en la raiz del proyecto:
```
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=localhost:1521/FREEPDB1
DB_USER=abogado
DB_PASSWORD=abogado123
```

7. Ejecutar el servidor de desarrollo:
```bash
python manage.py runserver
```

8. Acceder a la aplicacion:
```
http://localhost:8000/clientes/
```

## Estructura del Proyecto

```
InterfazBD1/
├── config/              # Configuracion de Django
│   ├── settings.py      # Configuracion principal
│   ├── urls.py          # URLs raiz
│   └── wsgi.py
├── clientes/            # Aplicacion principal
│   ├── templates/       # Plantillas HTML
│   ├── views.py         # Vistas (Controladores)
│   ├── urls.py          # URLs de la app
│   └── models.py        # (Vacio - se usa SQL Raw)
├── scripts/             # Scripts SQL
│   ├── 01_modelo.sql    # Esquema de la BD
│   └── 02_data.sql      # Datos de prueba
├── media/               # Archivos subidos (PDFs)
├── docker-compose.yml   # Configuracion Docker
├── Dockerfile           # Imagen de la app
└── requirements.txt     # Dependencias Python
```

## Uso del Sistema

### 1. Registro de Clientes

Acceder a la seccion "Registro Cliente" para:
- Buscar clientes existentes por codigo
- Crear nuevos clientes
- Actualizar informacion de clientes
- Eliminar clientes

### 2. Gestion de Casos

Acceder a "Gestion Caso" para:
- Buscar casos por numero
- Crear nuevos casos asociados a un cliente
- Ver historial de casos de un cliente
- Imprimir casos

### 3. Gestion de Expedientes

Acceder a "Gestion Expediente" para:
- Navegar entre etapas procesales de un caso
- Crear nuevos expedientes (etapas)
- Registrar sucesos y resultados
- Cargar documentos PDF
- Asignar abogados y entidades


## Licencia

Este proyecto es de uso academico.
