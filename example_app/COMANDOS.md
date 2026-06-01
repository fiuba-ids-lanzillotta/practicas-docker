# Comandos Útiles para Docker

## Construcción

# Construir la imagen
docker build -t ejemplo-flask:1.0 .

# Construir sin cache (fuerza recompilación)
docker build --no-cache -t ejemplo-flask:1.0 .

# Construir con etiquetas múltiples
docker build -t ejemplo-flask:1.0 -t ejemplo-flask:latest .

## Ejecución

# Ejecutar en modo interactivo
docker run -p 5505:5505 ejemplo-flask:1.0

# Ejecutar en background (-d = detached)
docker run -d -p 5505:5505 --name mi-app ejemplo-flask:1.0

# Ejecutar con variables de entorno
docker run -p 5505:5505 -e FLASK_ENV=production ejemplo-flask:1.0

# Ejecutar con volumen (para desarrollo)
docker run -p 5505:5505 -v $(pwd):/app ejemplo-flask:1.0

## Inspección

# Ver todas las imágenes
docker images

# Ver imágenes de este proyecto
docker images | grep ejemplo-flask

# Ver todos los contenedores (activos e inactivos)
docker ps -a

# Ver solo contenedores activos
docker ps

# Ver capas de la imagen
docker history ejemplo-flask:1.0

# Inspeccionar detalles de la imagen
docker inspect ejemplo-flask:1.0

## Logs

# Ver logs de un contenedor
docker logs <CONTAINER_ID>

# Seguir logs en tiempo real
docker logs -f <CONTAINER_ID>

# Ver últimas 50 líneas
docker logs --tail 50 <CONTAINER_ID>

## 🔧 Mantenimiento

# Entrar al contenedor en ejecución
docker exec -it <CONTAINER_ID> /bin/bash

# Ejecutar comando en contenedor
docker exec <CONTAINER_ID> pip list

# Parar contenedor
docker stop <CONTAINER_ID>

# Iniciar contenedor detenido
docker start <CONTAINER_ID>

# Eliminar contenedor
docker rm <CONTAINER_ID>

# Eliminar imagen
docker rmi ejemplo-flask:1.0

# Limpiar todo no usado
docker system prune

# Limpiar incluyendo volúmenes
docker system prune -a --volumes

## Testing

# Probar endpoint
curl http://localhost:5505/

# Probar API
curl http://localhost:5505/info

# Con verbose
curl -v http://localhost:5505/

# Salvar respuesta en archivo
curl http://localhost:5505/info > response.json
