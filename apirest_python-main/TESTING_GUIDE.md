# Guía de Pruebas con Herramientas de Testing

Esta guía te muestra cómo probar tu API REST usando diferentes herramientas de testing populares.

## Tabla de Contenidos
1. [Postman](#postman)
2. [Thunder Client (VSCode)](#thunder-client-vscode)
3. [HTTPie (Terminal)](#httpie-terminal)
4. [Python Requests (Script)](#python-requests-script)

---

## Postman

Postman es una de las herramientas más populares para probar APIs.

### Instalación

1. Descarga Postman desde: https://www.postman.com/downloads/
2. Instala y abre la aplicación

### Configuración Inicial

1. Crea una nueva **Collection** llamada "API Productos"
2. Agrega una variable de entorno:
   - Variable: `base_url`
   - Value: `http://localhost:4000`

### Crear Requests en Postman

#### 1. GET - Obtener todos los productos

```
Method: GET
URL: {{base_url}}/productos
Headers: (ninguno necesario)
Body: (vacío)
```

#### 2. POST - Crear producto

```
Method: POST
URL: {{base_url}}/productos
Headers:
  - Content-Type: application/json
Body (raw, JSON):
{
  "nombre": "Mouse Logitech",
  "precio": 25.99,
  "descripcion": "Mouse inalámbrico",
  "stock": 50
}
```

#### 3. PUT - Actualizar producto

```
Method: PUT
URL: {{base_url}}/productos/1
Headers:
  - Content-Type: application/json
Body (raw, JSON):
{
  "precio": 22.99,
  "stock": 45
}
```

#### 4. DELETE - Eliminar producto

```
Method: DELETE
URL: {{base_url}}/productos/1
Headers: (ninguno necesario)
Body: (vacío)
```

### Tests Automáticos en Postman

Puedes agregar tests automáticos en la pestaña "Tests" de cada request:

**Para GET /productos:**
```javascript
pm.test("Status code es 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Respuesta tiene productos", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.success).to.eql(true);
    pm.expect(jsonData).to.have.property('productos');
});
```

**Para POST /productos:**
```javascript
pm.test("Producto creado correctamente", function () {
    pm.response.to.have.status(201);
    var jsonData = pm.response.json();
    pm.expect(jsonData.success).to.eql(true);
    pm.expect(jsonData.producto).to.have.property('id');
});

// Guardar el ID para usarlo en otros tests
pm.test("Guardar ID del producto", function () {
    var jsonData = pm.response.json();
    pm.environment.set("producto_id", jsonData.producto.id);
});
```

**Para PUT /productos:**
```javascript
pm.test("Producto actualizado", function () {
    pm.response.to.have.status(200);
    var jsonData = pm.response.json();
    pm.expect(jsonData.success).to.eql(true);
});
```

**Para DELETE /productos:**
```javascript
pm.test("Producto eliminado", function () {
    pm.response.to.have.status(200);
    var jsonData = pm.response.json();
    pm.expect(jsonData.success).to.eql(true);
});
```

### Importar Collection a Postman

Puedes crear un archivo JSON con toda la collection. Guárdalo como `postman_collection.json`:

```json
{
  "info": {
    "name": "API Productos",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Obtener todos los productos",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "{{base_url}}/productos",
          "host": ["{{base_url}}"],
          "path": ["productos"]
        }
      }
    },
    {
      "name": "Crear producto",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"nombre\": \"Mouse Logitech\",\n  \"precio\": 25.99,\n  \"descripcion\": \"Mouse inalámbrico\",\n  \"stock\": 50\n}"
        },
        "url": {
          "raw": "{{base_url}}/productos",
          "host": ["{{base_url}}"],
          "path": ["productos"]
        }
      }
    },
    {
      "name": "Actualizar producto",
      "request": {
        "method": "PUT",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"precio\": 22.99,\n  \"stock\": 45\n}"
        },
        "url": {
          "raw": "{{base_url}}/productos/1",
          "host": ["{{base_url}}"],
          "path": ["productos", "1"]
        }
      }
    },
    {
      "name": "Eliminar producto",
      "request": {
        "method": "DELETE",
        "header": [],
        "url": {
          "raw": "{{base_url}}/productos/1",
          "host": ["{{base_url}}"],
          "path": ["productos", "1"]
        }
      }
    }
  ]
}
```

Importa este archivo en Postman: `Import > File > Selecciona postman_collection.json`

---

## Thunder Client (VSCode)

Thunder Client es una extensión ligera de VSCode para probar APIs.

### Instalación

1. Abre VSCode
2. Ve a Extensions (Ctrl+Shift+X)
3. Busca "Thunder Client"
4. Instala la extensión

### Uso

1. Haz clic en el icono de Thunder Client en la barra lateral
2. Crea una nueva **Collection** llamada "API Productos"

### Crear Requests

#### GET - Obtener productos

```
Method: GET
URL: http://localhost:4000/productos
```

Click en "Send"

#### POST - Crear producto

```
Method: POST
URL: http://localhost:4000/productos
Headers:
  Content-Type: application/json
Body (JSON):
{
  "nombre": "Teclado Mecánico",
  "precio": 89.99,
  "descripcion": "Teclado mecánico RGB",
  "stock": 20
}
```

#### PUT - Actualizar producto

```
Method: PUT
URL: http://localhost:4000/productos/1
Headers:
  Content-Type: application/json
Body (JSON):
{
  "precio": 79.99,
  "stock": 18
}
```

#### DELETE - Eliminar producto

```
Method: DELETE
URL: http://localhost:4000/productos/1
```

### Variables de Entorno en Thunder Client

1. Click en "Env" (ambiente)
2. Crea un nuevo ambiente "Local"
3. Agrega variable:
   ```
   base_url = http://localhost:4000
   ```
4. Usa en requests: `{{base_url}}/productos`

### Exportar/Importar Collection

Thunder Client permite exportar la collection como JSON:
1. Click derecho en la collection
2. "Export Collection"
3. Guarda el archivo

Para importar:
1. Click en "Collections"
2. Click en los tres puntos
3. "Import Collection"

---

## HTTPie (Terminal)

HTTPie es una herramienta de línea de comandos más amigable que curl.

### Instalación

```bash
# Ubuntu/Debian
sudo apt install httpie

# Fedora
sudo dnf install httpie

# macOS
brew install httpie

# pip (cualquier sistema)
pip install httpie
```

### Ejemplos de Uso

#### GET - Obtener productos

```bash
http GET http://localhost:4000/productos
```

#### POST - Crear producto

```bash
http POST http://localhost:4000/productos \
  nombre="Monitor Samsung" \
  precio:=299.99 \
  descripcion="Monitor 24 pulgadas" \
  stock:=15
```

Nota: `:=` indica que el valor es un número, no string.

#### PUT - Actualizar producto

```bash
http PUT http://localhost:4000/productos/1 \
  precio:=279.99 \
  stock:=12
```

#### DELETE - Eliminar producto

```bash
http DELETE http://localhost:4000/productos/1
```

### Opciones útiles de HTTPie

```bash
# Ver solo el body de la respuesta
http -b GET http://localhost:4000/productos

# Ver solo los headers
http -h GET http://localhost:4000/productos

# Verbose (ver request y response completos)
http -v POST http://localhost:4000/productos nombre="Test" precio:=99 stock:=10

# Guardar respuesta en archivo
http GET http://localhost:4000/productos > productos.json

# Pretty print con colores
http --pretty=all GET http://localhost:4000/productos
```

---

## Python Requests (Script)

Ya incluimos un script completo de pruebas en `test_api.py`, pero aquí hay ejemplos adicionales para usar interactivamente.

### Script Interactivo

Crea un archivo `test_manual.py`:

```python
import requests
import json

BASE_URL = 'http://localhost:4000'

def obtener_productos():
    """Obtener todos los productos"""
    response = requests.get(f'{BASE_URL}/productos')
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    return response.json()

def crear_producto(nombre, precio, descripcion, stock):
    """Crear un nuevo producto"""
    data = {
        "nombre": nombre,
        "precio": precio,
        "descripcion": descripcion,
        "stock": stock
    }
    response = requests.post(
        f'{BASE_URL}/productos',
        json=data,
        headers={'Content-Type': 'application/json'}
    )
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    return response.json()

def actualizar_producto(producto_id, **kwargs):
    """Actualizar un producto existente"""
    response = requests.put(
        f'{BASE_URL}/productos/{producto_id}',
        json=kwargs,
        headers={'Content-Type': 'application/json'}
    )
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    return response.json()

def eliminar_producto(producto_id):
    """Eliminar un producto"""
    response = requests.delete(f'{BASE_URL}/productos/{producto_id}')
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    return response.json()

# Ejemplos de uso
if __name__ == '__main__':
    print("=== OBTENER PRODUCTOS ===")
    obtener_productos()

    print("\n=== CREAR PRODUCTO ===")
    resultado = crear_producto(
        nombre="Auriculares Sony",
        precio=149.99,
        descripcion="Auriculares inalámbricos con cancelación de ruido",
        stock=30
    )

    # Si se creó exitosamente, obtener el ID
    if resultado.get('success'):
        producto_id = resultado['producto']['id']

        print(f"\n=== ACTUALIZAR PRODUCTO {producto_id} ===")
        actualizar_producto(producto_id, precio=139.99, stock=28)

        print(f"\n=== ELIMINAR PRODUCTO {producto_id} ===")
        eliminar_producto(producto_id)
```

### Uso Interactivo con Python REPL

```bash
python3
```

```python
import requests

# GET
r = requests.get('http://localhost:4000/productos')
print(r.json())

# POST
data = {"nombre": "Test", "precio": 99.99, "stock": 10}
r = requests.post('http://localhost:4000/productos', json=data)
print(r.json())

# PUT
r = requests.put('http://localhost:4000/productos/1', json={"precio": 89.99})
print(r.json())

# DELETE
r = requests.delete('http://localhost:4000/productos/1')
print(r.json())
```

---

## Comparación de Herramientas

| Herramienta | Tipo | Ventajas | Desventajas |
|-------------|------|----------|-------------|
| **Postman** | GUI | Muy completa, tests automáticos, documentación | Pesada, requiere instalación |
| **Thunder Client** | VSCode Extension | Integrada en VSCode, ligera | Menos features que Postman |
| **HTTPie** | CLI | Rápida, sintaxis simple | Solo línea de comandos |
| **Python Requests** | Código | Automatizable, flexible | Requiere escribir código |
| **curl** | CLI | Disponible en todo sistema | Sintaxis compleja |

---

## Recomendaciones

1. **Para desarrollo rápido:** Thunder Client (si usas VSCode)
2. **Para testing completo:** Postman con tests automáticos
3. **Para CI/CD:** Script Python (`test_api.py`)
4. **Para comandos rápidos:** HTTPie o curl

---

## Solución de Problemas

### Error: Connection refused

```bash
# Verifica que el servidor esté corriendo
ps aux | grep python

# Inicia el servidor
python app.py
```

### Error: Port already in use

```bash
# Encuentra el proceso usando el puerto 4000
lsof -i :4000

# Mata el proceso (reemplaza PID)
kill -9 PID
```

### Error: ModuleNotFoundError

```bash
# Activa el ambiente virtual
source venv/bin/activate

# Instala las dependencias
pip install -r requirements.txt
```

---

## Recursos Adicionales

- [Documentación de Postman](https://learning.postman.com/docs/)
- [Thunder Client Docs](https://www.thunderclient.com/docs)
- [HTTPie Docs](https://httpie.io/docs)
- [Python Requests Docs](https://requests.readthedocs.io/)
