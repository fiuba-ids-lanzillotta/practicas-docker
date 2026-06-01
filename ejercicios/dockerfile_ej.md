# Crear un Dockerfile paso a paso

En este ejercicio aprenderás a crear Dockerfiles desde cero. El archivo `Dockerfile` está **vacío** y se va a completar a medida que hagas cada uno de los pasos explicados en este documento.

---

## Tabla de Contenidos

1. [¿Qué es un Dockerfile?](#qué-es-un-dockerfile)
2. [Preparar la Aplicación Flask](#preparar-la-aplicación-flask)
3. [Construir el Dockerfile - Línea por Línea](#construir-el-dockerfile---línea-por-línea)
4. [Entender las Capas de Docker](#entender-las-capas-de-docker)
5. [Copiar TODO vs Lo Esencial](#copiar-todo-vs-lo-esencial)
6. [Paso a Paso: Construir y Ejecutar](#paso-a-paso-construir-y-ejecutar)
7. [Ejercicios Adicionales](#ejercicios-adicionales)
8. [Troubleshooting](#troubleshooting)

---

## ¿Qué es un Dockerfile?

Un **Dockerfile** es un archivo de texto que contiene instrucciones para construir una imagen Docker. Piénsalo como una "receta" que le dice a Docker cómo empaquetar tu aplicación.

**Analogía:**
```
Receta de cocina       →  Ingredientes + pasos = plato final
Dockerfile            →  Imagen base + instrucciones = imagen Docker
```

**¿Por qué?**
- Reproducibilidad: Todos obtienen la misma imagen
- Portabilidad: Funciona igual en dev, staging, producción
- Automatización: No necesitas configurar manualmente cada servidor
- Versionado: Puedes trackear cambios en Git

---

## Preparar la Aplicación Flask

Antes de crear el Dockerfile, verificá que tenés la carpeta `example_app` con estos archivos:

```bash
example_app/
├── app.py                  # Flask app (ya existe)
├── requirements.txt        # Dependencias (ya existe)
├── Dockerfile             # ← VACÍO (aquí agregarás código)
├── .dockerignore          # Ya existe
├── templates/
│   └── index.html         # Ya existe
└── static/
    └── style.css          # Ya existe
```

### Verifica los archivos existen

```bash
cd example_app
ls -la
cat app.py
cat requirements.txt
```

---

## Construir el Dockerfile - Línea por Línea

Ahora tenés que agregar las instrucciones al archivo `Dockerfile` vacío. Sigue cada paso cuidadosamente.

### PASO 1: Agregar la Imagen Base

**¿Qué es?** La imagen base contiene el S.O. y herramientas preinstaladas.

**¿Por qué Python 3.11-slim?**
- `python:3.11-slim` es optimizada (180 MB vs 900 MB de la completa)
- Perfecta para producción
- Incluye Python 3.11 y pip

**Agrega esto al Dockerfile vacío:**

```dockerfile
FROM python:3.11-slim
```

**¿Qué pasa?**
- Docker descargará la imagen base de Python 3.11-slim
- Es el punto de partida para nuestra imágen

---

### PASO 2: Establecer Directorio de Trabajo

**¿Qué es?** El directorio donde se ejecutarán los comandos posteriores.

**Agrega:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app
```

**¿Qué pasa?**
- Crea `/app` dentro del contenedor
- Todos los comandos posteriores se ejecutarán desde esta carpeta
- Es como hacer `mkdir /app && cd /app`

**¿Por qué es importante?**
- Mantiene la imagen organizada
- Evita conflictos con otros directorios
- Facilita mantenimiento

---

### PASO 3: Copiar `requirements.txt` (ANTES de copiar todo)


**Agrega:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
```

**¿Por qué copiamos solo requirements.txt primero?**
- `requirements.txt` cambia poco (no es muy frecuente agregar librerías todo el tiempo)
- El código `app.py` cambia frecuentemente (cada día)
- Docker cachea capas: si cambias solo código, no reinstala paquetes
- Esto ahorra **MUCHO TIEMPO** en builds posteriores

---

### PASO 4: Instalar Dependencias

**Agrega:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
```

**¿Qué hace?**
- `RUN` ejecuta comandos dentro del contenedor
- `--no-cache-dir` ahorra espacio (pip no guarda paquetes descargados)

**¿Por qué después de COPY requirements.txt?**
- Necesita el archivo para instalar los paquetes listados

---

### PASO 5: Copiar Todo el Código

**Agrega:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
```

**¿Qué hace?**
- `COPY . .` copia TODOS los archivos del host al contenedor
- Primer `.` = tu directorio actual
- Segundo `.` = `/app` (porque establecimos WORKDIR)

**¿Por qué DESPUÉS de instalar dependencias?**
- El código cambia frecuentemente
- Si copiáramos todo primero, Docker reinstalaría paquetes cada vez que cambies `app.py`
- Ahora, al cambiar código, solo se copia (muy rápido), no se reinstalan paquetes

---

### PASO 6: Documentar el Puerto

**Agrega:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5505
```

**¿Qué hace?**
- `EXPOSE` documenta que la app escucha en puerto 5505
- **Importante:** NO publica automáticamente
- Para publicar usas: `docker run -p 5505:5505 imagen`

**¿Por qué?**
- Es documentación para otros desarrolladores
- Se ve en `docker inspect` y `docker port`

---

### PASO 7: Definir el Comando de Inicio

**Agrega (línea final):**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5505

CMD ["python", "app.py"]
```

**¿Qué hace?**
- `CMD` define el comando que se ejecuta cuando inicia el contenedor
- Se ejecuta DESPUÉS de construir la imagen

**¿Forma correcta?**
- CMD ["python", "app.py"] (exec form - recomendado)
- CMD python app.py (shell form - evita)

**¿Por qué?** En exec form, `python` recibe señales del contenedor (SIGTERM), permitiendo shutdown limpio.

---

## Entender las Capas de Docker

### ¿Qué son las capas?

Docker construye tu imagen en **capas**. Cada instrucción (FROM, RUN, COPY) crea una nueva capa.

```
CAPA 7:  CMD ["python", "app.py"]                     0 B
CAPA 6:  EXPOSE 5505                                  0 B
CAPA 5:  COPY . .                                     5.2 kB
CAPA 4:  RUN pip install --no-cache-dir -r ...       42 MB   ← Pesada
CAPA 3:  COPY requirements.txt .                      200 B
CAPA 2:  WORKDIR /app                                 0 B
CAPA 1:  FROM python:3.11-slim (base)                 130 MB
─────────────────────────────────────────────────────────────
TOTAL:                                                ~177 MB
```

### ¿Por qué importan las capas?

**1. Caché de Docker:**
```dockerfile
# Primera build: ejecuta TODO
docker build -t app:1.0 .   # Toma 45 segundos

# Segunda build (sin cambios): reutiliza todas las capas
docker build -t app:1.0 .   # Toma 1 segundo (muy rápido)

# Cambias app.py y reconstruyes
docker build -t app:1.0 .   # Reutiliza capas 1-3, regenera 5-7
                             # Toma 5 segundos (la capa 4 NO se regenera)
```

**2. Tamaño de la imagen:**
Cada capa suma al tamaño. Las capas grandes son costosas.

**3. Carga cuando ejecutas:**
Docker carga todas las capas en memoria.

---

## Copiar TODO vs Lo Esencial

Este es el concepto **MÁS IMPORTANTE** del ejercicio. La diferencia entre dos enfoques:

### Error: Copiar TODO primero

```dockerfile
FROM python:3.11-slim
WORKDIR /app

COPY . .                                    # ← Copias TODO

RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5505
CMD ["python", "app.py"]
```

**¿Qué contiene COPY . .?**
- `app.py`
- `requirements.txt`
- `templates/`
- `static/`
- `.git/` (si no hay .dockerignore)
- `__pycache__/` (si no hay .dockerignore)
- `*.pyc` archivos compilados
- Cualquier otro archivo

**¿Qué pasa cuando cambias app.py?**

```bash
# Primera build
docker build -t app:1.0 .                  # 45 segundos
# Se cachean todas las capas

# Cambias app.py (1 línea)
nano app.py

# Reconstruyes
docker build -t app:1.0 .                  # PROBLEMA: 45 segundos de nuevo!
# ¿Por qué? Porque COPY . . cambió
# Docker invalida las capas posteriores (incluyendo RUN pip...)
# ¡Reinstala TODOS los paquetes de nuevo aunque no cambiaron!
```

**Capas:**
```
CAPA 3: RUN pip install ... (REGENERADA - toma 40 segundos)  Innecesario
CAPA 2: COPY . .            (REGENERADA - rápido)
CAPA 1: FROM + WORKDIR      (cached)
```

---

### Correcto: Copiar requirements.txt primero

```dockerfile
FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .                    # ← Solo dependencias

RUN pip install --no-cache-dir -r requirements.txt

COPY . .                                   # ← Luego el código

EXPOSE 5505
CMD ["python", "app.py"]
```

**¿Qué pasa cuando cambias app.py?**

```bash
# Primera build
docker build -t app:1.0 .                  # 45 segundos
# Se cachean todas las capas

# Cambias app.py (1 línea)
nano app.py

# Reconstruyes
docker build -t app:1.0 .                  # ÉXITO: 3 segundos (muy rápido)
# ¿Por qué? Porque COPY requirements.txt no cambió
# Docker mantiene en caché la capa de pip install
# Solo regenera COPY . . (muy rápido, solo copia archivos)
```

**Capas:**
```
CAPA 5: COPY . .            (REGENERADA - muy rápido)
CAPA 4: RUN pip install ... (CACHED - 0 segundos)       Reutilizada!
CAPA 3: COPY requirements.txt . (CACHED)
CAPA 2: WORKDIR /app        (CACHED)
CAPA 1: FROM               (CACHED)
```

**Diferencia:** 45 segundos vs 3 segundos. **15x más rápido** en desarrollo.

### ¿Y el .dockerignore?

Para evitar copiar archivos innecesarios, usa `.dockerignore`:

```
__pycache__
*.pyc
*.pyo
.git
.gitignore
.env
*.log
.DS_Store
node_modules/
venv/
.venv
```

**Beneficios:**
- Imagen más pequeña
- Build más rápido (menos archivos a copiar)
- Evitas secretos en `.env` dentro de la imagen

---

## Paso a Paso: Construir y Ejecutar

### 1. Verifica el Dockerfile esté completo

---

### 2. Construir la Imagen

```bash
docker build -t ejemplo-flask:1.0 .
```

**¿Qué hace?**
- Lee el `Dockerfile` actual (`.`)
- Ejecuta cada instrucción
- Crea capas y cachea
- Crea imagen `ejemplo-flask:1.0`

**Salida esperada:**
```
Sending build context to Docker daemon  3.072kB
Step 1/7 : FROM python:3.11-slim
 ---> abc123 (Downloaded)
Step 2/7 : WORKDIR /app
 ---> Running in xyz789...
Step 3/7 : COPY requirements.txt .
 ---> Running in xyz789...
Step 4/7 : RUN pip install --no-cache-dir...
 ---> Running in xyz789...
Step 5/7 : COPY . .
 ---> Running in xyz789...
Step 6/7 : EXPOSE 5505
 ---> Running in xyz789...
Step 7/7 : CMD ["python", "app.py"]
 ---> Running in xyz789...
Successfully tagged ejemplo-flask:1.0
```

**Nota:** Toma ~1 min la primera vez (descarga Python, instala paquetes).

---

### 3. Verificar la imagen

```bash
docker images
```

```
REPOSITORY           TAG    IMAGE ID      CREATED      SIZE
ejemplo-flask        1.0    abc123def456  2 minutes    150MB
```

---

### 4. Ver las capas creadas

```bash
docker history ejemplo-flask:1.0
```

**¿Qué ves?** Cada instrucción del Dockerfile como una capa:

```
IMAGE      CREATED     CREATED BY                    SIZE
abc123     2 min ago   CMD ["python" "app.py"]       0B
def456     2 min ago   EXPOSE 5505                   0B
ghi789     2 min ago   COPY . .                      5.2kB
jkl012     2 min ago   RUN pip install ...           42MB (La más pesada)
mno345     2 min ago   COPY requirements.txt .       200B
pqr678     2 min ago   WORKDIR /app                  0B
stu901     3 weeks ago FROM python:3.11-slim         130MB
```

---

### 5. Ejecutar un contenedor

```bash
docker run -p 5505:5505 ejemplo-flask:1.0
```

**Salida esperada:**
```
 * Serving Flask app 'app'
 * Debug mode: off
 * Running on http://0.0.0.0:5505
 * Press CTRL+C to quit
```

**La aplicación está corriendo!** La terminal está ocupada; mantén abierta esta ventana.

---

### 6. Probar la aplicación (en otra terminal)

**Opción A: Navegador**
```
http://localhost:5505/
```

Deberías ver una landing page hermosa con estilos.

**Opción B: Terminal**
```bash
# Ver HTML
curl http://localhost:5505/

# Ver API JSON
curl http://localhost:5505/info
```

**Respuesta esperada:**
```json
{
  "message": "Esta es una API simple",
  "status": "running",
  "version": "1.0"
}
```

---

### 7. Ver contenedores activos

En otra terminal:

```bash
docker ps
```

```
CONTAINER ID  IMAGE                STATUS      PORTS
abc123def456  ejemplo-flask:1.0    Up 2 mins   0.0.0.0:5505->5505/tcp
```

---

### 8. Parar el contenedor

En la terminal donde corre Flask, presiona `Ctrl+C`.

O desde otra terminal:

```bash
docker stop <CONTAINER_ID>
```

---

## Ejercicios Propuestos

### Ejercicio 1: Probar el Caché

**Objetivo:** Demostrar que cambiar código reutiliza capas.

**Pasos:**

1. Construye por primera vez (mide el tiempo):
```bash
time docker build -t ejemplo-flask:1.0 .
```
Nota el tiempo total (ej: ~45 seg).

2. Reconstruye sin cambios:
```bash
time docker build -t ejemplo-flask:1.0 .
```
Mucho más rápido (~1-2 seg), todas las capas del caché.

3. Cambia `app.py` (cualquier pequeño cambio, ej: el título):
```bash
nano app.py  # Cambia algo, guarda
```

4. Reconstruye:
```bash
time docker build -t ejemplo-flask:1.0 .
```
¿Toma 45 seg o 3 seg? Si configuraste correctamente, ~3 seg.

---

### Ejercicio 2: Cambiar Puerto

**Objetivo:** Modificar app y Dockerfile para usar puerto 8080.

**Pasos:**

1. Edita `app.py`, línea final:
```python
# Cambiar:
app.run(debug=False, host='0.0.0.0', port=5505)

# A:
app.run(debug=False, host='0.0.0.0', port=8080)
```

2. Edita `Dockerfile`, línea EXPOSE:
```dockerfile
# Cambiar:
EXPOSE 5505

# A:
EXPOSE 8080
```

3. Reconstruye:
```bash
docker build -t ejemplo-flask:1.1 .
```

4. Ejecuta:
```bash
docker run -p 8080:8080 ejemplo-flask:1.1
```

5. Prueba:
```bash
curl http://localhost:8080/
```

---

### Ejercicio 3: Comparar Imágenes Base

**Objetivo:** Ver diferencia de tamaño entre -slim y -alpine.

**Pasos:**

1. Crea `Dockerfile.alpine` con esta línea de diferencia:
```dockerfile
FROM python:3.11-alpine    # Cambia solo esto
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5505
CMD ["python", "app.py"]
```

2. Construye:
```bash
docker build -f Dockerfile.alpine -t ejemplo-flask:alpine .
```

3. Compara tamaños:
```bash
docker images | grep ejemplo-flask
```

**Resultado esperado:**
```
REPOSITORY           TAG           SIZE
ejemplo-flask        1.0           150MB   (slim)
ejemplo-flask        alpine        50MB    (alpine)
```

**Conclusión:** Alpine es 3x más pequeño. ¿Por qué no siempre usarlo?
- Alpine usa `musl` en lugar de `glibc` (menos compatible)
- Algunos paquetes Python necesitan compilación (más lento)
- Para microservicios está bien; para apps complejas, `-slim`

---

### Ejercicio 4: Agregar Variables de Entorno

**Objetivo:** Usar ENV en el Dockerfile.

**Pasos:**

1. Edita `Dockerfile` e inserta después de WORKDIR:
```dockerfile
FROM python:3.11-slim
WORKDIR /app

ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
# ... resto del Dockerfile
```

2. Reconstruye:
```bash
docker build -t ejemplo-flask:1.2 .
```

3. Verifica que se establecieron:
```bash
docker inspect ejemplo-flask:1.2 | grep -A 5 Env
```

**¿Qué hacen?**
- `FLASK_ENV=production` → Desactiva debug mode
- `PYTHONUNBUFFERED=1` → Muestra logs inmediatamente (sin buffering)

---

### Ejercicio 5: Health Check

**Objetivo:** Que Docker verifique que la app está sana.

**Pasos:**

1. Edita `Dockerfile` e inserta después de EXPOSE:
```dockerfile
EXPOSE 5505

HEALTHCHECK --interval=30s --timeout=3s --start-period=40s \
    CMD python -c "import requests; requests.get('http://localhost:5505/')" || exit 1

CMD ["python", "app.py"]
```

2. Reconstruye:
```bash
docker build -t ejemplo-flask:1.3 .
```

3. Ejecuta:
```bash
docker run -p 5505:5505 ejemplo-flask:1.3
```

4. En otra terminal, verifica:
```bash
docker ps
```

Busca en la columna `STATUS` algo como `healthy` o `unhealthy`.

---

### Ejercicio 6: Multi-stage Build (Avanzado)

**Objetivo:** Crear imagen más pequeña sin archivos innecesarios.

**Concepto:** Usa contenedor "builder" para compilar, luego copia solo lo necesario.

**Pasos:**

1. Crea `Dockerfile.multistage`:
```dockerfile
# STAGE 1: Builder (temporal)
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# STAGE 2: Runtime (imagen final)
FROM python:3.11-alpine
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
EXPOSE 5505
CMD ["python", "app.py"]
```

2. Construye:
```bash
docker build -f Dockerfile.multistage -t ejemplo-flask:multistage .
```

3. Compara tamaños:
```bash
docker images | grep ejemplo-flask
```

**Resultado esperado:**
```
REPOSITORY           TAG              SIZE
ejemplo-flask        1.0              150MB   (slim, normal)
ejemplo-flask        alpine           50MB    (alpine)
ejemplo-flask        multistage       45MB    (multistage + alpine, más pequeño)
```

**Ventaja:** Sin `pip`, sin `gcc`, solo el código Python ejecutable.

---

## Troubleshooting

### Error: "Dockerfile: No such file or directory"

```bash
# Verifica estar en la carpeta correcta
pwd
# Debe ser: /Users/tommy/Documents/practicas-docker/example_app

# Verifica que existe
ls -la Dockerfile

# Si no existe, crea uno vacío
touch Dockerfile
```

---

### Error: "Port already in use"

```bash
# Error: bind: address already in use

# Solución 1: Usa otro puerto
docker run -p 8000:5505 ejemplo-flask:1.0

# Solución 2: Ver quién ocupa puerto 5505
lsof -i :5505

# Solución 3: Parar contenedor viejo
docker stop <CONTAINER_ID>
```

---

### Error: "Cannot find module Flask"

```bash
# Error: ModuleNotFoundError: No module named 'flask'

# Verifica que requirements.txt se copió
docker exec <CONTAINER_ID> cat /app/requirements.txt

# Verifica que pip instaló
docker exec <CONTAINER_ID> pip list | grep Flask

# Si no está, reconstruye desde cero
docker build --no-cache -t ejemplo-flask:1.0 .
```

---

### Error: Ver logs para debugging

```bash
# Logs del contenedor
docker logs <CONTAINER_ID>

# Seguir logs en tiempo real
docker logs -f <CONTAINER_ID>

# Últimas 50 líneas
docker logs --tail 50 <CONTAINER_ID>

# Entrar al contenedor
docker exec -it <CONTAINER_ID> /bin/bash

# Dentro del contenedor:
ls -la /app
cat requirements.txt
python app.py  # Prueba ejecutar manualmente
```

---

### Error: Limpiar imágenes/contenedores

```bash
# Ver todo
docker ps -a
docker images

# Eliminar contenedor específico
docker rm <CONTAINER_ID>

# Eliminar imagen
docker rmi ejemplo-flask:1.0

# Limpiar todo no usado
docker system prune

# Limpiar TODO (incluyendo volúmenes)
docker system prune -a --volumes
```

---

## Referencia Rápida

### Construcción
```bash
docker build -t nombre:tag .              # Normal
docker build --no-cache -t nombre:tag .   # Sin caché
docker build -f Dockerfile.alt -t nombre . # Dockerfile alternativo
```

### Ejecución
```bash
docker run -p 5505:5505 nombre:tag       # Interactivo
docker run -d -p 5505:5505 nombre:tag    # Background
docker run -e VAR=val nombre:tag         # Con env var
docker run -v $(pwd):/app nombre:tag     # Con volumen
```

### Inspección
```bash
docker images                             # Ver imágenes
docker ps                                 # Contenedores activos
docker ps -a                              # Todos
docker history nombre:tag                 # Capas
docker inspect nombre:tag                 # Detalles
docker logs <ID>                          # Logs
```

### Mantenimiento
```bash
docker stop <ID>                          # Parar
docker rm <ID>                            # Eliminar
docker exec -it <ID> /bin/bash           # Entrar
```

---

## Resumen: Lo que Aprendiste

[FROM] --> Imagen base (python:3.11-slim)  
[WORKDIR] --> Directorio `/app`  
[COPY requirements.txt] --> Copiar dependencias PRIMERO (caché)  
[RUN pip install] --> Instalar paquetes  
[COPY . .] --> Copiar código DESPUÉS  
[EXPOSE] --> Documentar puerto  
[CMD] --> Comando de inicio  

[Capas] --> Cada instrucción crea una capa  
[Caché] --> Docker reutiliza capas no modificadas  
[Orden importa] --> Afecta velocidad de builds  

[Construcción] --> `docker build -t nombre:tag .`  
[Ejecución] --> `docker run -p 5505:5505 nombre:tag`  

---

## Siguientes Pasos?

- Experimenta con los 6 ejercicios propuestos
- Crea Dockerfiles para tus propias aplicaciones
- Aprende Docker Compose para múltiples contenedores
- Explora registros (Docker Hub, ECR, GCR)

**Felicidades! Ahora entiendes Dockerfiles profesionalmente.**
