# Proyecto: API REST con Docker, FastAPI y PostgreSQL

## Descripción
Este proyecto consiste en el diseño y desarrollo de una API REST utilizando **FastAPI** para acceder y gestionar datos almacenados en una base de datos relacional (**PostgreSQL**). Todo el entorno se ejecuta en contenedores utilizando **Docker**, proporcionando un sistema escalable y fácil de configurar.

La API permite realizar operaciones CRUD (Crear, Leer, Actualizar y Eliminar) en una tabla llamada `my_movies` dentro del dataset `my_collections`. La configuración incluye dos contenedores: uno para la API y otro para la base de datos.

---

## Características

### Contenedores:
1. **API**: Contenedor basado en **FastAPI** desarrollado por el estudiante.
2. **Base de Datos**: Contenedor basado en **PostgreSQL** utilizando una imagen oficial de Docker Hub.

### Base de Datos:
- Dataset: `my_collections`
- Tabla: `my_movies`
  - Campos:
    - `ID` (secuencial)
    - `Autor` (cadena de texto)
    - `Descripción` (cadena de texto, representa el nombre de la película)
    - `Fecha de Estreno` (fecha)

Adicionalmente, se incluye un archivo `init.sql` para inicializar la base de datos con la siguiente estructura y datos de prueba:

```sql
-- 1) Creación de base de datos
CREATE DATABASE my_collections;

-- 2) Creación de tablas
CREATE TABLE my_movies (
    ID SERIAL PRIMARY KEY,         -- Campo ID, autoincrementable
    Autor VARCHAR(100),            -- Campo Autor, cadena de texto
    Descripcion TEXT,              -- Campo Descripción, texto largo
    Fecha_Estreno DATE             -- Campo Fecha de Estreno, tipo fecha
);

-- 3) Inserción de registros de prueba a la tabla creada
INSERT INTO my_movies (Autor, Descripcion, Fecha_Estreno)
VALUES 
    ('Steven Spielberg', 'Raiders of the Lost Ark', '1981-06-12'),
    ('Christopher Nolan', 'Inception', '2010-07-16'),
    ('Quentin Tarantino', 'Django Unchained', '2012-08-17'),
    ('James Cameron', 'Titanic', '1997-12-19'),
    ('Ridley Scott', 'Blade Runner', '1982-06-25');
```

---

## Funcionalidades de la API

### Estructura y funcionalidad del archivo principal (`main.py`):
El archivo `main.py` contiene la implementación de los métodos que interactúan con la base de datos utilizando **FastAPI** y `psycopg2`. Cada endpoint realiza operaciones CRUD en la tabla `my_movies`:

1. **GET**: Lee los datos de la tabla `my_movies`. Puede obtener todos los registros o uno específico mediante su `ID`.
   ```python
   @app.get("/movies")
   def read_items():
       cur = conn.cursor()
       cur.execute("SELECT * FROM my_movies")
       rows = cur.fetchall()
       cur.close()
       return {"items": rows}
   ```

2. **POST**: Inserta un nuevo registro en la tabla con los datos proporcionados por el usuario. El `ID` se genera automáticamente.
   ```python
   @app.post("/movies")
   def create_items(item: Item):
       cur = conn.cursor()
       cur.execute("INSERT INTO my_movies (autor, descripcion, fecha_estreno) VALUES (%s, %s, %s)", (item.autor, item.descripcion, item.fecha_estreno))
       conn.commit()
       cur.close()
       return {"item": item}
   ```

3. **PUT**: Actualiza uno o más campos de un registro existente identificado por su `ID`.
   ```python
   @app.put("/movies/{movie_id}")
   def put_item(movie_id: int, item: Item):
       cur = conn.cursor()
       cur.execute("UPDATE my_movies SET autor = %s, descripcion = %s, fecha_estreno = %s WHERE id = %s", (item.autor, item.descripcion, item.fecha_estreno, movie_id))
       conn.commit()
       cur.close()
       return {"item": item}
   ```

4. **DELETE**: Elimina un registro específico de la tabla identificado por su `ID`.
   ```python
   @app.delete("/movies/{movie_id}")
   def delete_item(movie_id: int):
       cur = conn.cursor()
       cur.execute("DELETE FROM my_movies WHERE id = %s", (movie_id,))
       conn.commit()
       cur.close()
       return {"item_id": movie_id}
   ```

Estos métodos aseguran que la base de datos se mantenga actualizada y permiten una interacción sencilla y clara mediante los endpoints de la API.

---

## Requisitos

### Tecnologías:
- **Docker** (para contenedores)
- **FastAPI** (para la API)
- **PostgreSQL** (para la base de datos)

### Dependencias:
- Archivo `requirements.txt` para la API con las siguientes bibliotecas:
  ```
  fastapi
  uvicorn
  psycopg2
  ```

---

## Configuración del Entorno

### Paso 1: Clonar el repositorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_REPOSITORIO>
```

### Paso 2: Crear y configurar los contenedores con Docker
1. **Base de datos**:
    ```bash
    docker run --name trabajo-postgres \
      -e POSTGRES_USER=tu_usuario \
      -e POSTGRES_PASSWORD=tu_password \
      -e POSTGRES_DB=my_collections \
      -v $(pwd)/init.sql:/docker-entrypoint-initdb.d/init.sql \
      -p 5432:5432 -d postgres
    ```

2. **API**:
    Ya se cuenta con el archivo `Dockerfile`:
    ```dockerfile
    # Step 1: Use official lightweight Python image as base OS.
    FROM tiangolo/uvicorn-gunicorn:python3.8-slim

    # Step 2. Copy local code to the container image.
    WORKDIR /app
    COPY . .

    # Step 3. Install production dependencies.
    RUN pip install -r requirements.txt

    # Step 4: Run the web service on container startup using gunicorn webserver.
    ENV PORT=8080
    CMD gunicorn app2:app  --bind 0.0.0.0:$PORT --worker-class uvicorn.workers.UvicornWorker
    ```
    Luego, construir y ejecutar el contenedor:
    ```bash
    docker build -t trabajo-fastapi .
    docker run --name trabajo-fastapi -p 8080:8080 --link trabajo-postgres:db -d trabajo-fastapi
    ```

---

## Uso de la API

### Endpoints disponibles:
1. **GET**: `http://localhost:8080/movies`
   - Obtiene todos los registros de la tabla `my_movies`.

2. **POST**: `http://localhost:8080/movies`
   - Inserta un nuevo registro enviando un cuerpo JSON como este:
     ```json
     {
       "autor": "Nombre del Autor",
       "descripcion": "Nombre de la Película",
       "fecha_estreno": "2024-12-14"
     }
     ```

3. **PUT**: `http://localhost:8080/movies/{id}`
   - Actualiza un registro existente con un cuerpo JSON similar al anterior.

4. **DELETE**: `http://localhost:8080/movies/{id}`
   - Elimina el registro con el `ID` especificado.

---

## Ejecución de FastAPI localmente
Si deseas ejecutar la API sin Docker, utiliza el siguiente comando en la raíz del proyecto:
```bash
uvicorn main:app --reload
```
Esto habilitará un entorno de desarrollo local para interactuar con la API en `http://127.0.0.1:8000`.

---

## Autor
Proyecto desarrollado por **Fernando Cunza**.