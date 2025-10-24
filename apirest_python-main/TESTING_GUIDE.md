# Guía de Pruebas con Herramientas de Testing

## Postman
Postman es una de las herramientas más populares para probar APIs.

## Instalación
Descarga Postman desde: https://www.postman.com/downloads/

Instala y abre la aplicación

## Configuración Inicial
Crea una nueva Collection llamada "API Personas"

Agrega una variable de entorno:

Variable: base_url

Value: http://localhost:4000

## Crear Requests en Postman
1. GET - Obtener todas las personas
Method: GET
URL: {{base_url}}/personas
Headers: (ninguno necesario)
Body: (vacío)
2. POST - Crear persona
Method: POST
URL: {{base_url}}/personas
Headers:
  - Content-Type: application/json
Body (raw, JSON):
{
  "nombre": "María",
  "apellido": "González",
  "edad": 28,
  "email": "maria.gonzalez@email.com",
  "telefono": "+1234567890",
  "direccion": "Calle Principal 123",
  "fecha_nacimiento": "1995-05-15"
}
3. PUT - Actualizar persona

Method: PUT
URL: {{base_url}}/personas/1
Headers:
  - Content-Type: application/json
Body (raw, JSON):
{
  "edad": 29,
  "email": "maria.gonzalez.nueva@email.com"
}
4. DELETE - Eliminar persona

Method: DELETE
URL: {{base_url}}/personas/1
Headers: (ninguno necesario)
Body: (vacío)

## Tests automaticos en Postman

Puedes agregar tests automáticos en la pestaña "Tests" de cada request:

Para GET /personas:

pm.test("Status code es 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Respuesta tiene personas", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.success).to.eql(true);
    pm.expect(jsonData).to.have.property('personas');
});

Para POST /personas:

pm.test("Persona creada correctamente", function () {
    pm.response.to.have.status(201);
    var jsonData = pm.response.json();
    pm.expect(jsonData.success).to.eql(true);
    pm.expect(jsonData.persona).to.have.property('id');
});

// Guardar el ID para usarlo en otros tests
pm.test("Guardar ID de la persona", function () {
    var jsonData = pm.response.json();
    pm.environment.set("persona_id", jsonData.persona.id);
});

Para PUT /personas:

pm.test("Persona actualizada", function () {
    pm.response.to.have.status(200);
    var jsonData = pm.response.json();
    pm.expect(jsonData.success).to.eql(true);
});

Para DELETE /personas:

pm.test("Persona eliminada", function () {
    pm.response.to.have.status(200);
    var jsonData = pm.response.json();
    pm.expect(jsonData.success).to.eql(true);
});

## Importar collection a postman

Puedes crear un archivo JSON con toda la collection. Guárdalo como postman_collection.json:

{
  "info": {
    "name": "API Personas",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Obtener todas las personas",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "{{base_url}}/personas",
          "host": ["{{base_url}}"],
          "path": ["personas"]
        }
      }
    },
    {
      "name": "Crear persona",
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
          "raw": "{\n  \"nombre\": \"María\",\n  \"apellido\": \"González\",\n  \"edad\": 28,\n  \"email\": \"maria.gonzalez@email.com\",\n  \"telefono\": \"+1234567890\",\n  \"direccion\": \"Calle Principal 123\",\n  \"fecha_nacimiento\": \"1995-05-15\"\n}"
        },
        "url": {
          "raw": "{{base_url}}/personas",
          "host": ["{{base_url}}"],
          "path": ["personas"]
        }
      }
    },
    {
      "name": "Actualizar persona",
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
          "raw": "{\n  \"edad\": 29,\n  \"email\": \"maria.gonzalez.nueva@email.com\"\n}"
        },
        "url": {
          "raw": "{{base_url}}/personas/1",
          "host": ["{{base_url}}"],
          "path": ["personas", "1"]
        }
      }
    },
    {
      "name": "Eliminar persona",
      "request": {
        "method": "DELETE",
        "header": [],
        "url": {
          "raw": "{{base_url}}/personas/1",
          "host": ["{{base_url}}"],
          "path": ["personas", "1"]
        }
      }
    }
  ]
}
Importa este archivo en Postman: Import > File > Selecciona postman_collection.json

## Thunder client (VScode)

Thunder Client es una extensión ligera de VSCode para probar APIs.

## Instalación
Abre VSCode

Ve a Extensions (Ctrl+Shift+X)

Busca "Thunder Client"

Instala la extensión

## Uso
Haz clic en el icono de Thunder Client en la barra lateral

Crea una nueva Collection llamada "API Personas"

## Crear Requests
GET - Obtener personas

Method: GET
URL: http://localhost:4000/personas

Click en "Send"

## POST - Crear persona

Method: POST
URL: http://localhost:4000/personas
Headers:
  Content-Type: application/json
Body (JSON):
{
  "nombre": "Carlos",
  "apellido": "López",
  "edad": 35,
  "email": "carlos.lopez@email.com",
  "telefono": "+0987654321",
  "direccion": "Avenida Central 456",
  "fecha_nacimiento": "1988-08-20"
}

## PUT - Actualizar persona

Method: PUT
URL: http://localhost:4000/personas/1
Headers:
  Content-Type: application/json
Body (JSON):
{
  "edad": 36,
  "telefono": "+1111111111"
}

## DELETE - Eliminar persona

Method: DELETE
URL: http://localhost:4000/personas/1

## Variables de Entorno en Thunder Client

Click en "Env" (ambiente)

Crea un nuevo ambiente "Local"

Agrega variable:
base_url = http://localhost:4000

Usa en requests: {{base_url}}/personas

## Exportar/Importar Collection

Thunder Client permite exportar la collection como JSON:

Click derecho en la collection

"Export Collection"

Guarda el archivo

## Para importar:

Click en "Collections"

Click en los tres puntos

"Import Collection"

## HTTPie (Terminal)
HTTPie es una herramienta de línea de comandos más amigable que curl.

# INSTALACIÓN

# Ubuntu/Debian
sudo apt install httpie

# Fedora
sudo dnf install httpie

# macOS
brew install httpie

# pip (cualquier sistema)
pip install httpie

# EJEMPLOS DE USO

## GET - Obtener personas

http GET http://localhost:4000/personas

## POST - Crear persona

http POST http://localhost:4000/personas \
  nombre="Ana" \
  apellido="Martínez" \
  edad:=25 \
  email="ana.martinez@email.com" \
  telefono="+5555555555" \
  direccion="Plaza Mayor 789" \
  fecha_nacimiento="1998-03-10"

  
# Nota: := indica que el valor es un número, no string.

## PUT - Actualizar persona

http PUT http://localhost:4000/personas/1 \
  edad:=26 \
  direccion="Nueva Dirección 123"

## DELETE - Eliminar persona

http DELETE http://localhost:4000/personas/1

# Opciones útiles de HTTPie
# Ver solo el body de la respuesta
http -b GET http://localhost:4000/personas

# Ver solo los headers
http -h GET http://localhost:4000/personas

# Verbose (ver request y response completos)
http -v POST http://localhost:4000/personas nombre="Test" apellido="User" edad:=30

# Guardar respuesta en archivo
http GET http://localhost:4000/personas > personas.json

# Pretty print con colores
http --pretty=all GET http://localhost:4000/personas

# Script interactivo

Crea un archivo test_manual.py:
---------------------------------------
import requests
import json

BASE_URL = 'http://localhost:4000'

def obtener_personas():
    """Obtener todas las personas"""
    response = requests.get(f'{BASE_URL}/personas')
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    return response.json()

def crear_persona(nombre, apellido, edad, email="", telefono="", direccion="", fecha_nacimiento=""):
    """Crear una nueva persona"""
    data = {
        "nombre": nombre,
        "apellido": apellido,
        "edad": edad,
        "email": email,
        "telefono": telefono,
        "direccion": direccion,
        "fecha_nacimiento": fecha_nacimiento
    }
    response = requests.post(
        f'{BASE_URL}/personas',
        json=data,
        headers={'Content-Type': 'application/json'}
    )
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    return response.json()

def actualizar_persona(persona_id, **kwargs):
    """Actualizar una persona existente"""
    response = requests.put(
        f'{BASE_URL}/personas/{persona_id}',
        json=kwargs,
        headers={'Content-Type': 'application/json'}
    )
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    return response.json()

def eliminar_persona(persona_id):
    """Eliminar una persona"""
    response = requests.delete(f'{BASE_URL}/personas/{persona_id}')
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    return response.json()

# Ejemplos de uso
if __name__ == '__main__':
    print("=== OBTENER PERSONAS ===")
    obtener_personas()

    print("\n=== CREAR PERSONA ===")
    resultado = crear_persona(
        nombre="Pedro",
        apellido="Ramírez",
        edad=32,
        email="pedro.ramirez@email.com",
        telefono="+4444444444",
        direccion="Calle Secundaria 456",
        fecha_nacimiento="1991-12-01"
    )

    # Si se creó exitosamente, obtener el ID
    if resultado.get('success'):
        persona_id = resultado['persona']['id']

        print(f"\n=== ACTUALIZAR PERSONA {persona_id} ===")
        actualizar_persona(persona_id, edad=33, direccion="Nueva Dirección 999")

        print(f"\n=== ELIMINAR PERSONA {persona_id} ===")
        eliminar_persona(persona_id)

#### ---------

# Uso interactivo con python REPL

Python3

# Campos obligatorios

Recuerda que los campos obligatorios para crear una persona son:

nombre (string)

apellido (string)

edad (número entero)

Los campos opcionales son:

email (string)

telefono (string)

direccion (string)

fecha_nacimiento (string en formato YYYY-MM-DD)

## Recursos Adicionales

- [Documentación de Postman](https://learning.postman.com/docs/)
- [Thunder Client Docs](https://www.thunderclient.com/docs)
- [HTTPie Docs](https://httpie.io/docs)
- [Python Requests Docs](https://requests.readthedocs.io/)
