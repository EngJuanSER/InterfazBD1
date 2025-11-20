# Sistema de Gestion de Clientes - Django + Oracle

Interfaz web desarrollada en Django para realizar operaciones CRUD sobre un sistema de gestion legal con 14 tablas interrelacionadas en una base de datos Oracle.

## Inicio Rapido con Docker (Metodo Recomendado)

La forma mas rapida y sencilla de ejecutar el proyecto es usando Docker Compose. Este metodo configura y conecta todos los servicios automaticamente sin necesidad de instalar dependencias en su maquina local.

### Requisitos

- Docker 20.10 o superior
- Docker Compose 2.0 o superior
- Git

### Pasos de Instalacion

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/EngJuanSER/InterfazBD1.git
    cd InterfazBD1
    ```

2.  **Crear el archivo de variables de entorno:**
    Puedes copiar la plantilla de ejemplo. No es necesario modificarla para el entorno Docker.
    ```bash
    cp .env.example .env
    ```

3.  **Levantar los servicios:**
    Este comando construira las imagenes y arrancara los contenedores en segundo plano.
    ```bash
    docker compose up -d --build
    ```
    La primera vez, la base de datos puede tardar entre 30 y 60 segundos en inicializarse completamente.

4.  **Verificar que todo este corriendo:**
    ```bash
    docker compose ps
    ```
    Deberias ver dos servicios en estado `running` o `healthy`: `oracle-db` y `django-app`.

5.  **Acceder a la aplicacion:**
    Abre tu navegador y visita: **[http://localhost:8000/clientes/](http://localhost:8000/clientes/)**

Con estos pasos, el sistema esta completamente funcional.

### Arquitectura y Flujo Automatico

-   **Contenedores**: El sistema se compone de dos servicios: `django-app` (la aplicacion web) y `oracle-db` (la base de datos). Ambos se comunican a traves de una red Docker privada.
-   **Inicializacion**: Al arrancar por primera vez, el contenedor de Oracle ejecuta automaticamente los scripts de la carpeta `./scripts` en orden alfabetico. El script `00_init.sh` se asegura de que el esquema de la base de datos (`01_schema.sql`) y los datos de prueba (`02_data.sql`) se carguen en el esquema del usuario `abogado`, que tambien se crea automaticamente.
-   **Sincronizacion**: El contenedor de Django espera a que la base de datos este completamente lista (`healthy`) antes de iniciar, evitando errores de conexion.

### Comandos Utiles de Docker Compose

```bash
# Ver logs de todos los contenedores en tiempo real
docker compose logs -f

# Ver logs solo del contenedor de Django
docker compose logs -f django-app

# Detener los servicios (los datos se conservan)
docker compose down

# Detener servicios Y ELIMINAR todos los datos de la base de datos
docker compose down -v

# Reiniciar los servicios
docker compose restart

# Ejecutar un comando dentro del contenedor de Django
docker compose exec django-app python manage.py shell

# Conectarse a la base de datos Oracle directamente
docker compose exec oracle-db sqlplus abogado/abogado123@FREEPDB1
```

## Uso de la Aplicacion

### Buscar Cliente

1.  Ingresar el ID del cliente (numero entero).
2.  Hacer clic en el boton de busqueda.
3.  Los datos del cliente se cargan en el formulario.
4.  El campo de ID queda bloqueado para evitar la edicion accidental de otro registro.

### Crear Cliente

1.  Hacer clic en "Limpiar" para asegurar que el campo ID este vacio.
2.  Completar todos los campos requeridos.
3.  Hacer clic en "Guardar". El sistema asignara un ID automaticamente.

### Actualizar Cliente

1.  Buscar un cliente por su ID.
2.  Modificar los campos necesarios en el formulario.
3.  Hacer clic en "Guardar".

### Eliminar Cliente

1.  Buscar un cliente por su ID.
2.  Hacer clic en "Eliminar".
3.  Confirmar la eliminacion en el dialogo del navegador.

### Limpiar Formulario

Hacer clic en "Limpiar" para vaciar todos los campos y desbloquear el campo de ID para una nueva busqueda o creacion.

## Apendice A: Estructura del Proyecto

```
InterfazBD1/
├── docker-compose.yml           # Orquestacion de servicios Docker
├── Dockerfile                   # Definicion de la imagen de Django
├── entrypoint.sh                # Script de inicio del contenedor Django
├── requirements.txt             # Dependencias de Python
├── .env.example                 # Plantilla de variables de entorno
├── README.md                    # Este archivo
├── clientes/                    # Aplicacion principal de Django
│   ├── models.py                # 14 modelos de la base de datos
│   ├── views.py                 # Logica de las vistas (CRUD)
│   ├── forms.py                 # Formulario de Cliente
│   ├── urls.py                  # Rutas de la aplicacion
│   └── ...
└── scripts/
    ├── 00_init.sh               # Script de inicializacion de la BD
    ├── 01_schema.sql            # Script de creacion de tablas
    └── 02_data.sql              # Script de insercion de datos de prueba
```

## Apendice B: Instalacion Manual (Avanzado)

Esta seccion es para usuarios que deseen ejecutar la aplicacion Django localmente pero usando la base de datos en Docker.

1.  **Instalar dependencias locales**: Sigue los pasos de la documentacion oficial para instalar Python 3.11, Oracle Instant Client 21c y las dependencias de `requirements.txt`.
2.  **Iniciar solo la base de datos**:
    ```bash
    docker compose up -d oracle-db
    ```
3.  **Modificar archivo `.env`**: Cambia la variable `DB_NAME` para que apunte a `localhost`.
    ```env
    # .env
    DB_NAME=localhost:1521/FREEPDB1
    ```
4.  **Ejecutar migraciones de Django**:
    ```bash
    python manage.py migrate
    ```
5.  **Iniciar el servidor de desarrollo local**:
    ```bash
    python manage.py runserver
    ```

## Autor

Juan Serrano - EngJuanSER

## Licencia

Proyecto academico - Base de Datos I
