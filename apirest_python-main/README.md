# API REST de Gestión de Productos

API REST desarrollada con Flask y SQLite para gestionar un catálogo de productos. Implementa un CRUD completo (Crear, Leer, Actualizar, Eliminar).

## Características

- **Framework:** Flask 3.0
- **Base de datos:** SQLite
- **Puerto por defecto:** 4000
- **Formato de datos:** JSON

## Estructura de Datos

Cada producto contiene los siguientes campos:

```json
{
  "id": 1,
  "nombre": "Laptop Dell",
  "precio": 850.99,
  "descripcion": "Laptop Dell Inspiron 15",
  "stock": 10,
  "fecha_creacion": "2025-10-23 10:30:00"
}
```

## Instalación

### 1. Crear ambiente virtual

```bash
# Crear el ambiente virtual
python3 -m venv venv

# Activar el ambiente virtual (Linux/Mac)
source venv/bin/activate

# Activar el ambiente virtual (Windows)
venv\Scripts\activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar el servidor

```bash
python app.py
```

El servidor estará disponible en `http://localhost:4000`

## Endpoints de la API

### 1. Obtener todos los productos

**GET** `/productos`

**Respuesta exitosa (200):**
```json
{
  "success": true,
  "productos": [
    {
      "id": 1,
      "nombre": "Laptop Dell",
      "precio": 850.99,
      "descripcion": "Laptop Dell Inspiron 15",
      "stock": 10,
      "fecha_creacion": "2025-10-23 10:30:00"
    }
  ]
}
```

**Ejemplo curl:**
```bash
curl http://localhost:4000/productos
```

---

### 2. Crear un nuevo producto

**POST** `/productos`

**Body (JSON):**
```json
{
  "nombre": "Laptop Dell",
  "precio": 850.99,
  "descripcion": "Laptop Dell Inspiron 15",
  "stock": 10
}
```

**Campos requeridos:** `nombre`, `precio`, `stock`
**Campos opcionales:** `descripcion`

**Respuesta exitosa (201):**
```json
{
  "success": true,
  "producto": {
    "id": 1,
    "nombre": "Laptop Dell",
    "precio": 850.99,
    "descripcion": "Laptop Dell Inspiron 15",
    "stock": 10
  }
}
```

**Ejemplo curl:**
```bash
curl -X POST http://localhost:4000/productos \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Laptop Dell",
    "precio": 850.99,
    "descripcion": "Laptop Dell Inspiron 15",
    "stock": 10
  }'
```

---

### 3. Actualizar un producto

**PUT** `/productos/<id>`

**Body (JSON):** (todos los campos son opcionales)
```json
{
  "nombre": "Laptop HP",
  "precio": 799.99,
  "descripcion": "Laptop HP actualizada",
  "stock": 8
}
```

**Respuesta exitosa (200):**
```json
{
  "success": true,
  "message": "Producto actualizado correctamente"
}
```

**Respuesta error - Producto no encontrado (404):**
```json
{
  "success": false,
  "error": "Producto no encontrado"
}
```

**Ejemplo curl:**
```bash
curl -X PUT http://localhost:4000/productos/1 \
  -H "Content-Type: application/json" \
  -d '{
    "precio": 799.99,
    "stock": 8
  }'
```

---

### 4. Eliminar un producto

**DELETE** `/productos/<id>`

**Respuesta exitosa (200):**
```json
{
  "success": true,
  "message": "Producto eliminado correctamente"
}
```

**Respuesta error - Producto no encontrado (404):**
```json
{
  "success": false,
  "error": "Producto no encontrado"
}
```

**Ejemplo curl:**
```bash
curl -X DELETE http://localhost:4000/productos/1
```

## Pruebas Automatizadas

Este proyecto incluye un script de pruebas automatizado que verifica todos los endpoints de la API.

### Ejecutar las pruebas

1. Asegúrate de que el servidor esté corriendo:
```bash
python app.py
```

2. En otra terminal, ejecuta el script de pruebas:
```bash
python test_api.py
```

El script ejecutará automáticamente:
- Verificación de conexión al servidor
- Tests de lectura (GET)
- Tests de creación (POST) con datos válidos e inválidos
- Tests de actualización (PUT) con IDs existentes e inexistentes
- Tests de eliminación (DELETE) con IDs existentes e inexistentes

## Códigos de Estado HTTP

| Código | Descripción |
|--------|-------------|
| 200    | OK - Operación exitosa |
| 201    | Created - Recurso creado exitosamente |
| 400    | Bad Request - Datos inválidos |
| 404    | Not Found - Recurso no encontrado |
| 500    | Internal Server Error - Error del servidor |

## Estructura del Proyecto

```
apirest_python/
│
├── app.py                 # Archivo principal de la aplicación
├── productos.db           # Base de datos SQLite (se crea automáticamente)
├── requirements.txt       # Dependencias del proyecto
├── test_api.py           # Script de pruebas automatizadas
├── README.md             # Este archivo
├── TESTING_GUIDE.md      # Guía de pruebas con Postman y Thunder Client
└── venv/                 # Ambiente virtual (no incluido en git)
```

## Base de Datos

La base de datos SQLite se crea automáticamente al iniciar la aplicación. La tabla `productos` tiene la siguiente estructura:

```sql
CREATE TABLE productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL,
    descripcion TEXT,
    stock INTEGER NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Manejo de Errores

Todos los endpoints incluyen manejo de errores y retornan respuestas en formato JSON con la estructura:

```json
{
  "success": false,
  "error": "Descripción del error"
}
```

## Desactivar el Ambiente Virtual

Cuando termines de trabajar, desactiva el ambiente virtual:

```bash
deactivate
```

## Tecnologías Utilizadas

- **Python 3.x**
- **Flask 3.0** - Framework web
- **SQLite3** - Base de datos
- **Requests** - Para pruebas HTTP (en test_api.py)

## Autor

Creado con Flask y SQLite

## Licencia

Este proyecto es de código abierto y está disponible para uso educativo.
