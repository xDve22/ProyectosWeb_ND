# Description

Este proyecto utiliza Docker y Docker Compose para levantar un entorno de desarrollo de Django de manera rápida y consistente.

## Requisitos previos

Antes de empezar asegúrate de tener instalado en tu máquina:

- Docker: https://docs.docker.com/get-docker/
- Docker Compose: https://docs.docker.com/compose/install/

Puedes verificar las versiones con:

```bash
docker --version
docker compose version
```

## Levantar el proyecto

1. Construir la imagen de Docker ( solo la primera vez ):

```bash
docker compose build
```

2. Levantar el servicio:

```bash
docker compose up
```

Esto iniciará el servidor de Django dentro del contenedor.  
Por defecto estará disponible en:

http://localhost:8000

## Crear migraciones y aplicar cambios

Si necesitas correr migraciones:

```bash
docker compose run devjobs python manage.py makemigrations
docker compose run devjobs python manage.py migrate
```

## Crear un superusuario


```bash
docker compose run devjobs python manage.py createsuperuser
```

## Rutas disponibles
- Dashboard (ejemplo creado):  
  http://localhost:8000/dashboard/

## Detener el proyecto

```bash
docker compose down
```

O simplemente correr Ctrl + c

## Reconstruir el contenedor (si cambias dependencias)


```bash
docker compose build --no-cache
docker compose up
```

## Notas

- Los cambios en el código se reflejan automáticamente gracias a que Django corre en modo desarrollo.
- Si agregas nuevas dependencias en requirements.txt, debes reconstruir la imagen con:


```bash
docker compose build
```