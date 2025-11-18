# Sistema de Gestión de Clientes - Django + Oracle

Interfaz web desarrollada en Django para realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre clientes almacenados en Oracle Database.

## Descripción

Sistema web para gestión de clientes que incluye:
- Registro de nuevos clientes
- Búsqueda de clientes existentes por código
- Actualización de datos de clientes
- Eliminacion de clientes
- Tipos de documento almacenados en Oracle Database
- Interfaz responsiva con Bootstrap 5

## Tecnologías y Versiones Requeridas

### Software Base
- **Python:** 3.11 o superior
- **Django:** 5.2.8 o superior
- **Oracle Database:** 19c o superior (23c recomendado)
- **Oracle Instant Client:** 23.4 o superior
- **Docker:** 20.10+ (opcional, para base de datos local)

### Dependencias Python
```
django>=5.1.0          # Framework web
oracledb>=2.0.0        # Driver para Oracle Database
gunicorn>=21.0.0       # Servidor WSGI
python-decouple>=3.8   # Manejo de variables de entorno
whitenoise>=6.6.0      # Servir archivos estáticos
```

## Estructura del Proyecto

```
InterfazBD1/
├── config/                     # Configuración de Django
│   ├── settings.py            # Configuración principal
│   ├── urls.py                # URLs del proyecto
│   └── wsgi.py                # Punto de entrada WSGI
├── clientes/                   # Aplicación principal
│   ├── models.py              # Modelos (TipoDocumento, Cliente)
│   ├── views.py               # Vistas y lógica de negocio
│   ├── forms.py               # Formularios con validaciones
│   ├── urls.py                # URLs de la aplicación
│   └── templates/clientes/
│       └── registro_cliente.html
├── scripts/
│   └── create_tables.sql      # Script de creación de tablas
├── requirements.txt            # Dependencias Python
├── .env.example               # Plantilla de variables de entorno
├── .gitignore
├── manage.py                  # CLI de Django
└── README.md
```

## Modelo de Datos

### Tabla TipoDocumento
| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| idTipoDoc | VARCHAR2(2) | PRIMARY KEY | Código del tipo |
| descTipoDoc | VARCHAR2(30) | NOT NULL | Descripción |

### Tabla Cliente
| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| codCliente | VARCHAR2(5) | PRIMARY KEY | Código único |
| nomCliente | VARCHAR2(30) | NOT NULL | Nombre |
| apellCliente | VARCHAR2(30) | NOT NULL | Apellido |
| idTipoDoc | VARCHAR2(2) | FOREIGN KEY | Referencia a TipoDocumento |
| nDocumento | VARCHAR2(15) | NOT NULL | Número de documento |

## Instalación Paso a Paso

### 1. Clonar el Repositorio

```bash
git clone https://github.com/EngJuanSER/InterfazBD1.git
cd InterfazBD1
```

### 2. Crear Entorno Virtual

**Opción A: Con Conda**
```bash
conda create -n interfazbd python=3.11 -y
conda activate interfazbd
```

**Opción B: Con venv**
```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar Dependencias Python

```bash
pip install -r requirements.txt
```

### 4. Instalar Oracle Instant Client

Oracle Instant Client es **obligatorio** para conectarse a Oracle Database desde Python.

#### Linux (Ubuntu/Debian)

```bash
# Descargar Oracle Instant Client 23.4
wget https://download.oracle.com/otn_software/linux/instantclient/2340000/instantclient-basic-linux.x64-23.4.0.24.05.zip

# Crear directorio e instalar
sudo mkdir -p /opt/oracle
sudo unzip instantclient-basic-linux.x64-23.4.0.24.05.zip -d /opt/oracle

# Instalar dependencia libaio1
sudo apt-get install libaio1

# Configurar variable de entorno
echo 'export LD_LIBRARY_PATH=/opt/oracle/instantclient_23_4:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc
```

#### Windows

1. Descargar desde: https://www.oracle.com/database/technologies/instant-client/winx64-64-downloads.html
2. Descomprimir en: `C:\oracle\instantclient_23_4`
3. Agregar `C:\oracle\instantclient_23_4` al PATH del sistema
4. Instalar Visual C++ Redistributable: https://aka.ms/vs/17/release/vc_redist.x64.exe
5. Reiniciar la terminal

#### macOS

```bash
# Para Intel
curl -o instantclient.zip https://download.oracle.com/otn_software/mac/instantclient/234000/instantclient-basic-macos.x64-23.4.0.24.05.zip

# Para Apple Silicon (M1/M2)
curl -o instantclient.zip https://download.oracle.com/otn_software/mac/instantclient/234000/instantclient-basic-macos.arm64-23.4.0.24.05.zip

# Instalar
sudo mkdir -p /opt/oracle
sudo unzip instantclient.zip -d /opt/oracle

# Configurar variable de entorno
echo 'export DYLD_LIBRARY_PATH=/opt/oracle/instantclient_23_4:$DYLD_LIBRARY_PATH' >> ~/.zshrc
source ~/.zshrc
```

### 5. Configurar Oracle Database con Docker

**Crear y ejecutar contenedor:**

```bash
# Descargar imagen
docker pull gvenzl/oracle-free:latest

# Crear contenedor
docker run -d \
  --name oracle-23c \
  -p 1522:1521 \
  -e ORACLE_PASSWORD=abogado123 \
  -e APP_USER=abogado \
  -e APP_USER_PASSWORD=abogado123 \
  gvenzl/oracle-free:latest

# Verificar que esté corriendo
docker ps

# Ver logs (esperar mensaje: "DATABASE IS READY TO USE!")
docker logs -f oracle-23c
```

**Información de conexión:**
- Host: `localhost`
- Puerto: `1522`
- Servicio: `FREEPDB1`
- Usuario: `abogado`
- Contraseña: `abogado123`
- Cadena completa: `localhost:1522/FREEPDB1`

### 6. Crear Tablas en Oracle

**Copiar script al contenedor:**
```bash
docker cp scripts/create_tables.sql oracle-23c:/tmp/create_tables.sql
```

**Ejecutar script:**
```bash
docker exec -it oracle-23c sqlplus abogado/abogado123@FREEPDB1 @/tmp/create_tables.sql
```

El script crea:
- Tabla `TipoDocumento` con 5 tipos de documento (CC, CE, TI, PA, RC)
- Tabla `Cliente` con 5 clientes de ejemplo
- Relaciones de clave foránea

### 7. Configurar Variables de Entorno

**Copiar archivo de ejemplo:**
```bash
cp .env.example .env
```

**Editar el archivo `.env`:**
```env
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True

DB_NAME=localhost:1522/FREEPDB1
DB_USER=abogado
DB_PASSWORD=abogado123

ALLOWED_HOSTS=localhost,127.0.0.1
```

### 8. Ejecutar Migraciones de Django

Django necesita crear sus propias tablas para autenticación, sesiones y administración:

```bash
python manage.py migrate
```

**Opcional:** Crear superusuario para acceder al panel de administración:
```bash
python manage.py createsuperuser
```

### 9. Iniciar el Servidor

```bash
python manage.py runserver
```

Acceder a:
- **Aplicación de clientes:** http://localhost:8000/clientes/
- **Panel de administración:** http://localhost:8000/admin/

## Uso de la Aplicación

### Buscar Cliente Existente

1. Ingresar el código del cliente (ej: 00001)
2. Hacer clic en el botón de búsqueda (lupa) o presionar Enter
3. Si existe, los datos se cargan automáticamente en el formulario
4. El código queda bloqueado para evitar cambios accidentales

### Crear Nuevo Cliente

1. Ingresar un código nuevo (5 caracteres)
2. Completar nombre, apellido, tipo de documento y número
3. Hacer clic en "Guardar"
4. El sistema valida que no exista duplicado

### Actualizar Cliente

1. Buscar el cliente existente con la lupa
2. Modificar los campos que desee actualizar
3. Hacer clic en "Guardar"
4. El sistema detecta automáticamente que es una actualización

### Eliminar Cliente

1. Buscar el cliente existente con la lupa
2. Hacer clic en el botón "Eliminar" (rojo)
3. Confirmar la eliminación en el cuadro de diálogo
4. El registro se elimina permanentemente de la base de datos
5. El formulario se limpia automáticamente

**Nota:** El botón "Eliminar" solo aparece cuando se busca un cliente existente.

### Limpiar Formulario

Hacer clic en el botón "Limpiar" para vaciar todos los campos y comenzar de nuevo.

## Comandos Útiles de Docker

```bash
# Ver contenedores corriendo
docker ps

# Ver logs del contenedor
docker logs oracle-23c

# Detener contenedor
docker stop oracle-23c

# Iniciar contenedor
docker start oracle-23c

# Conectarse a SQL*Plus
docker exec -it oracle-23c sqlplus abogado/abogado123@FREEPDB1

# Reiniciar contenedor
docker restart oracle-23c
```

## Autor

Juan Serrano - [EngJuanSER](https://github.com/EngJuanSER)

## Licencia

Proyecto académico - Base de Datos I
