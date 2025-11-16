# Sistema de Gestión de Clientes

Interfaz web para operaciones CRUD de clientes con Oracle Database, desarrollada en Django.

## Descripción

Sistema web para registro y gestión de clientes que incluye:
- Registro de nuevos clientes
- Búsqueda de clientes por código
- Tipos de documento almacenados en base de datos
- Interfaz responsiva con Bootstrap 5

## Tecnologías

- Django 5.2.8
- Oracle Database
- Python 3.11+
- Bootstrap 5
- python-oracledb

## Estructura

```
InterfazBD1/
├── config/                 # Configuración Django
├── clientes/              # App principal (modelos, vistas, formularios)
├── scripts/               # Scripts SQL
└── requirements.txt       # Dependencias
```

## Instalación Local

```bash
# Clonar repositorio
git clone https://github.com/EngJuanSER/InterfazBD1.git
cd InterfazBD1

# Crear entorno virtual
conda create -n interfazbd python=3.11 -y
conda activate interfazbd

# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos en config/settings.py

# Ejecutar script SQL en Oracle
sqlplus usuario/contraseña@host:puerto/servicio @scripts/create_tables.sql

# Ejecutar servidor
python manage.py runserver
```

Acceder a: http://localhost:8000/clientes/

## Modelo de Datos

**TipoDocumento**
- idTipoDoc (PK): VARCHAR2(2)
- descTipoDoc: VARCHAR2(30)

**Cliente**
- codCliente (PK): VARCHAR2(5)
- nomCliente: VARCHAR2(30)
- apellCliente: VARCHAR2(30)
- idTipoDoc (FK): VARCHAR2(2)
- nDocumento: VARCHAR2(15)

## Configuración

### Local
Editar `config/settings.py` con las credenciales de Oracle.

### Producción
Copiar `.env.example` a `.env` y configurar las variables de entorno.

## Licencia

Proyecto académico
