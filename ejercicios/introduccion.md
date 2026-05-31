# Introducción a Docker - MySQL dentro de un contenedor
 
> En esta guía vamos a descargar una imagen desde DockerHub, instalarla y tenes a nuestra disposición una base de datos MySQL corriendo dentro de un Docker Container
---
 
## Objetivos
 
Al terminar esta guía vas a poder:
 
- Descargar una imagen oficial desde DockerHub.
- Levantar un contenedor de MySQL pasándole variables de configuración.
- Conectarte a la base de datos desde dentro del contenedor.
- Crear una base de datos, una tabla, e insertar y consultar datos.
- Apagar y limpiar el entorno cuando termines.
---
 
## Requisitos previos: instalar Docker
 
Antes de empezar necesitás tener Docker instalado. **Qué instalás depende de tu sistema operativo:**
 
| Sistema operativo | Opciones | Descarga oficial |
|---|---|---|
| **Linux** | **Docker Engine** (solo línea de comandos) **o** **Docker Desktop** (incluye también una interfaz gráfica) | Engine: <https://docs.docker.com/engine/install/> · Desktop: <https://www.docker.com/products/docker-desktop/> |
| **Windows** | **Solo Docker Desktop** | <https://www.docker.com/products/docker-desktop/> |
| **macOS** | **Solo Docker Desktop** | <https://www.docker.com/products/docker-desktop/> |
 
> 💡 **¿Engine o Desktop?** *Docker Engine* es el motor que corre los contenedores y se maneja 100% por terminal; está disponible **únicamente en Linux**. *Docker Desktop* es una aplicación con interfaz gráfica que ya incluye el motor adentro, y es la única opción en **Windows** y **macOS**. En **Linux** podés elegir cualquiera de las dos (para esta guía, con cualquiera alcanza).
 
Una vez instalado, abrí una terminal y verificá que funciona:
 
```bash
docker --version
```
 
> **Checkpoint 0:** Si el comando te devuelve una versión (por ejemplo `Docker version 27.x.x`), estás listo. Si da error, revisá la instalación antes de continuar. *(En Windows y macOS, asegurate de que la aplicación Docker Desktop esté abierta y en ejecución.)* Es probable que te salga algún mensaje de error diciendo que el comando docker no se encuentra dentro del sistema operativo, [esto es debido a que seguramente no incluíste a docker dentro del grupo de usuarios. ](https://docs.docker.com/engine/install/linux-postinstall/)
 
---
 
## 1Descargar la imagen de MySQL
 
Usamos `docker pull` para traer la imagen oficial desde [DockerHub](https://hub.docker.com). Vamos a fijar la versión `8.0` para que a todos nos funcione igual:
 
```bash
docker pull mysql:8.0
```
 
Verificá que la imagen quedó guardada en tu repositorio local:
 
```bash
docker images
```
 
> **Checkpoint 1:** En la salida de `docker images` tenés que ver una fila cuyo `REPOSITORY` sea `mysql` y cuyo `TAG` sea `8.0`.
 
> Extra: ¿Qué pasaría si en vez de `mysql:8.0` escribieras solo `mysql`?
 
---
 
## Poner en marcha el contenedor
 
Ahora creamos y arrancamos un contenedor a partir de la imagen. MySQL **necesita** que le indiquemos una contraseña para el usuario `root`; eso se hace con una variable de entorno (`-e`).
 
```bash
docker run --name mysql_fiuba -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 -d mysql:8.0
```
 
Desglose de los flags:
 
| Flag | Significado |
|---|---|
| `--name mysql_fiuba` | Le pone un nombre al contenedor para identificarlo fácil. |
| `-e MYSQL_ROOT_PASSWORD=root` | Define la contraseña del usuario `root` (acá usamos `root`). |
| `-p 3306:3306` | Publica el puerto: mapea el `3306` del contenedor al `3306` de tu máquina. |
| `-d` | *Detach*: el contenedor corre en segundo plano. |
| `mysql:8.0` | La imagen a partir de la cual se crea el contenedor. |
 
> La contraseña `root` es **solo por motivos prácticos**. En un entorno real nunca usarías una contraseña tan débil ni la dejarías escrita en un comando.
 
---
 
## Verificar que está corriendo
 
```bash
docker ps
```
 
> **Checkpoint 2:** Tenés que ver el contenedor `mysql_fiuba` en la lista, con el estado `Up ...`.
 
MySQL tarda unos segundos en inicializarse la primera vez. Si querés ver el progreso del arranque:
 
```bash
docker logs mysql_fiuba
```
 
> 🔍 Esperá hasta ver en los logs un mensaje similar a **"ready for connections"** antes de pasar al siguiente paso. Si el estado figura como `Restarting` o el contenedor desapareció de `docker ps`, revisá la sección de **Solución de problemas** al final.
 
---

## Conectarse al contenedor de MySQL

Usamos docker `docker exec` para ingresar dentro de la consola del contenedor.

`docker exec -it mysql_fiuba bin/bash` 

## Conectarse a MySQL
 
Una vez dentro, ejecutamos lo siguiente
 
```bash
mysql -u root -p
```
 
Te va a pedir la contraseña: escribí `root` y presioná Enter (no se ve mientras escribís, es normal).
 
> **Checkpoint 3:** Si todo salió bien, el prompt cambia a algo como:
>
> ```
> mysql>
> ```
>
 
---
 
## Crear una base de datos y una tabla
 
Ya estás dentro del prompt `mysql>`. Acá los comandos terminan con punto y coma `;`.
 
**a) Crear una base de datos y posicionarte en ella:**
 
```sql
CREATE DATABASE taller;
USE taller;
```
 
**b) Crear una tabla de ejemplo:**
 
```sql
CREATE TABLE alumnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    padron INT NOT NULL,
    aprobado BOOLEAN DEFAULT FALSE
);
```
 
**c) Verificá que la tabla se creó:**
 
```sql
SHOW TABLES;
DESCRIBE alumnos;
```
 
> **Checkpoint 4:** `SHOW TABLES;` tiene que listar la tabla `alumnos`, y `DESCRIBE alumnos;` te muestra sus columnas (`id`, `nombre`, `padron`, `aprobado`).
 
---
 
## Insertar y consultar datos (bonus)
 
```sql
INSERT INTO alumnos (nombre, padron, aprobado) VALUES
    ('Ada Lovelace', 100001, TRUE),
    ('Alan Turing', 100002, FALSE);
 
SELECT * FROM alumnos;
```
 
> ✅ **Checkpoint 5:** El `SELECT` te tiene que devolver una tabla con las dos filas que acabás de insertar.
 
---
 
## Salir, detener y limpiar
 
**a) Salir del cliente de MySQL** (volvés a la terminal de tu máquina):
 
```sql
exit
```
 
**b) Detener el contenedor** cuando termines de trabajar:
 
```bash
docker stop mysql_fiuba
```
 
**c) Eliminar el contenedor** (opcional, si ya no lo vas a usar):
 
```bash
docker rm mysql_fiuba
```
 
> **Para pensar:** Si hacés `docker stop` y después `docker start mysql_fiuba`, ¿siguen estando tu base `taller` y tu tabla `alumnos`? ¿Y si hacés `docker rm` y volvés a crear el contenedor con `docker run`? *(Pista: pensá dónde vive la información.)*
 
---
 
## Troubleshooting
 
| Síntoma | Posible causa y solución |
|---|---|
| `docker: command not found` | Docker no está instalado o no está en el PATH. |
| El contenedor aparece como `Restarting` o se cierra solo | Suele faltar la variable `MYSQL_ROOT_PASSWORD`. Eliminá el contenedor (`docker rm -f mysql_fiuba`) y volvé a correr el comando del Paso 2 completo. |
| `Access denied for user 'root'` | La contraseña no coincide con la que pusiste en `MYSQL_ROOT_PASSWORD`. Debe ser `root`. |
| `Can't connect` o "ready for connections" todavía no aparece | MySQL aún está inicializando. Esperá unos segundos y reintentá; verificá con `docker logs mysql_fiuba`. |
| `port is already allocated` (puerto 3306 ocupado) | Ya tenés otro MySQL usando el `3306`. Cambiá el mapeo, por ejemplo `-p 3307:3306`. |
| Estoy en Mac con chip Apple (M1/M2/M3) | La imagen `mysql:8.0` funciona; si tenés problemas, podés probar `docker pull mysql:8.0` igualmente o usar `mariadb` como alternativa compatible. |
 
---
 
## Resumen de comandos
 
```bash
docker pull mysql:8.0                                                   # Descargar la imagen
docker run --name mysql_fiuba -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 -d mysql:8.0   # Levantar el contenedor
docker ps                                                               # Verificar que corre
docker exec -it mysql_fiuba mysql -u root -p                            # Conectarse a MySQL
docker stop mysql_fiuba                                                 # Detenerlo
docker rm mysql_fiuba                                                   # Eliminarlo
```
 
```sql
CREATE DATABASE taller;        -- Crear base de datos
USE taller;                    -- Posicionarse en ella
CREATE TABLE alumnos (...);    -- Crear tabla
SHOW TABLES;                   -- Listar tablas
SELECT * FROM alumnos;         -- Consultar datos
```
