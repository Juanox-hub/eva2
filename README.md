# soporte-ti

Guía rápida para levantar el proyecto de Gestión de Incidencias con Django y MySQL.

## Requisitos

* Python 3.12+ y pip
* MySQL 8 (XAMPP o Workbench)
* Conector `mysqlclient`
* (Opcional) `virtualenv` o `venv` para aislar dependencias

## Paso a paso

1. Clona el repositorio y entra al directorio.
2. Crea y activa un entorno virtual (opcional pero recomendado):
   python -m venv venv
   venv\Scripts\activate
3. Instala dependencias:
   pip install -r requirements.txt

4.Configura la base de datos (ver sección siguiente).

5. Ejecuta migraciones:
   python manage.py makemigrations
   python manage.py migrate

6. (Opcional) crea un superusuario para administrar:
   python manage.py createsuperuser

7. Levanta el servidor de desarrollo:
   python manage.py runserver

## Configuración de Base de Datos
El proyecto requiere una base de datos MySQL llamada soporte_db (o el nombre que elijas). Asegúrate de que las credenciales en settings.py coincidan con tu configuración local:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'soporte_db',  # Crea esta base de datos en tu MySQL
        'USER': 'root',        # Tu usuario
        'PASSWORD': '',        # Tu contraseña
    }
}

## Configuracion Inicial (Roles)
Para que el sistema de permisos funcione correctamente, debes configurar el grupo de soporte:

1. Entra al admin (/admin) con tu superusuario.

2. Ve a Groups y crea un grupo llamado exactamente Soporte.

3. Los usuarios que pertenezcan a este grupo podrán ver y gestionar los casos asignados.

## Comandos útiles
-Crear migraciones de cambios en modelos: python manage.py makemigrations

-Aplicar migraciones pendientes: python manage.py migrate

-Crear superusuario: python manage.py createsuperuser

-Correr servidor: python manage.py runserver

## Notas

Los usuarios que se registran desde la web son "Clientes" por defecto.

Para convertir a un usuario en Técnico, debes agregarlo al grupo Soporte desde el panel de administración.

Recuerda tener el servicio de MySQL activo antes de correr el servidor.
