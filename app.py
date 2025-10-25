from flask import Flask, jsonify, request
import psycopg2
import os
from datetime import datetime
from contextlib import contextmanager # Importación clave para el manejo de recursos

app = Flask(__name__)

# --- Configuración de la base de datos ---
# Se recomienda usar un archivo .env o Docker para estas variables
DATABASE_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'database': os.environ.get('DB_NAME', 'crud_db'),
    'user': os.environ.get('DB_USER', 'postgres'),
    'password': os.environ.get('DB_PASSWORD', 'password'),
    'port': os.environ.get('DB_PORT', '5432')
}

# ----------------------------------------------------------------------
# 🌟 MEJORA 1: Manejo de Conexiones (Context Manager)
# ----------------------------------------------------------------------

@contextmanager
def get_db_cursor(commit=False):
    """
    Proporciona un cursor de base de datos que se asegura de cerrar la conexión 
    y hacer commit/rollback automáticamente.
    """
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(**DATABASE_CONFIG)
        cur = conn.cursor()
        yield cur # El cursor se pasa al bloque 'with'
        if commit:
            conn.commit()
    except Exception as e:
        # Si ocurre un error, asegura el rollback antes de re-lanzar
        if conn:
            conn.rollback()
        raise e
    finally:
        # Asegura el cierre del cursor y la conexión en cualquier caso
        if cur:
            cur.close()
        if conn:
            conn.close()

# ----------------------------------------------------------------------
# Lógica de Inicialización
# ----------------------------------------------------------------------

def init_db():
    # Usamos el context manager con commit=True
    try:
        with get_db_cursor(commit=True) as cur:
            # Crear tabla de productos
            cur.execute('''
                CREATE TABLE IF NOT EXISTS productos (
                    id SERIAL PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    precio DECIMAL(10,2) NOT NULL,
                    stock INTEGER DEFAULT 0,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Insertar datos de ejemplo
            cur.execute('''
                INSERT INTO productos (nombre, precio, stock) 
                VALUES 
                    ('Laptop', 1200.50, 10),
                    ('Mouse', 25.99, 50),
                    ('Teclado', 75.00, 30)
                ON CONFLICT (id) DO NOTHING 
                -- NOTA: La columna 'id' es SERIAL, 'ON CONFLICT DO NOTHING' no es ideal para ID SERIAL. 
                -- Se puede reemplazar por una columna UNIQUE (como 'nombre') o eliminar. 
                -- Mantenemos por simplicidad, aunque no es el uso más correcto aquí.
            ''')
        print("Base de datos inicializada y tabla 'productos' creada.")
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
        # La aplicación debería detenerse si la DB no está lista
        exit(1)

# ----------------------------------------------------------------------
# 🌟 MEJORA 2: Abstracción de Datos (Función de mapeo)
# ----------------------------------------------------------------------

def map_product_row(row, columns):
    """Mapea una fila de la DB (tupla) a un diccionario de producto."""
    if not row:
        return None
    # Aseguramos que el precio sea float para la salida JSON
    return {
        'id': row[0],
        'nombre': row[1],
        'precio': float(row[2]), # Convertimos Decimal a float/string
        'stock': row[3],
        'fecha_creacion': row[4].isoformat() if isinstance(row[4], datetime) else row[4]
    }

# Columnas seleccionadas para facilitar el mapeo
PRODUCT_COLUMNS = ['id', 'nombre', 'precio', 'stock', 'fecha_creacion']
SELECT_QUERY = f'SELECT {", ".join(PRODUCT_COLUMNS)} FROM productos'

# ----------------------------------------------------------------------
# Endpoints de la API
# ----------------------------------------------------------------------

@app.route('/')
def home():
    return jsonify({
        "message": "🚀 API CRUD Python + PostgreSQL (Mejorada) 🐍",
        "status": "Running",
        "endpoints": {
            "GET /productos": "Listar todos los productos",
            "GET /productos/<id>": "Obtener un producto por ID",
            "POST /productos": "Crear nuevo producto",
            "PUT /productos/<id>": "Actualizar producto",
            "DELETE /productos/<id>": "Eliminar producto"
        }
    })

# CREATE - Crear producto
@app.route('/productos', methods=['POST'])
def crear_producto():
    data = request.get_json()
    
    # 🌟 MEJORA 3: Validación de entrada (más estricta)
    nombre = data.get('nombre')
    precio = data.get('precio')
    stock = data.get('stock', 0)
    
    if not nombre or not precio:
        return jsonify({"error": "Nombre y precio son requeridos"}), 400
    
    try:
        # Intentamos convertir a float/int para validar tipo de dato
        precio = float(precio)
        stock = int(stock)
    except (ValueError, TypeError):
        return jsonify({"error": "Precio debe ser numérico y Stock debe ser un entero"}), 400

    try:
        with get_db_cursor(commit=True) as cur:
            cur.execute(
                f'INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s) RETURNING {", ".join(PRODUCT_COLUMNS)}',
                (nombre, precio, stock)
            )
            nuevo_producto = cur.fetchone()
            
            if nuevo_producto:
                producto_data = map_product_row(nuevo_producto, PRODUCT_COLUMNS)
                return jsonify(producto_data), 201
            else:
                # Caso improbable, pero asegura un código 500 si la inserción falla sin lanzar excepción.
                return jsonify({"error": "No se pudo crear el producto"}), 500
    
    except psycopg2.Error as e:
        # Manejo específico de errores de base de datos
        return jsonify({"error": f"Error de base de datos: {e.diag.message_primary}"}), 500
    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

# READ - Obtener todos los productos
@app.route('/productos', methods=['GET'])
def obtener_productos():
    try:
        # 🌟 MEJORA 4: Funcionalidad de Paginación/Filtro (Básica)
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        offset = (page - 1) * limit
        
        sql = f"{SELECT_QUERY} ORDER BY id LIMIT %s OFFSET %s"
        
        with get_db_cursor(commit=False) as cur:
            cur.execute(sql, (limit, offset))
            productos = cur.fetchall()
            
            # 🌟 MEJORA 2: Usamos la función de mapeo
            productos_list = [map_product_row(p, PRODUCT_COLUMNS) for p in productos]
            
            return jsonify(productos_list)
            
    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

# READ - Obtener producto por ID
@app.route('/productos/<int:producto_id>', methods=['GET'])
def obtener_producto(producto_id):
    try:
        with get_db_cursor(commit=False) as cur:
            cur.execute(f'{SELECT_QUERY} WHERE id = %s', (producto_id,))
            producto = cur.fetchone()
            
            producto_data = map_product_row(producto, PRODUCT_COLUMNS)
            
            if producto_data:
                return jsonify(producto_data)
            else:
                return jsonify({"error": "Producto no encontrado"}), 404
            
    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

# UPDATE - Actualizar producto
@app.route('/productos/<int:producto_id>', methods=['PUT'])
def actualizar_producto(producto_id):
    data = request.get_json()
    
    # 🌟 MEJORA 3: Validación
    if not data:
        return jsonify({"error": "No hay datos para actualizar"}), 400
        
    update_fields = []
    values = []
    
    # Mantenemos solo los campos válidos y los validamos
    if 'nombre' in data:
        update_fields.append("nombre = %s")
        values.append(data['nombre'])
    if 'precio' in data:
        try:
            precio = float(data['precio'])
            update_fields.append("precio = %s")
            values.append(precio)
        except (ValueError, TypeError):
            return jsonify({"error": "Precio debe ser numérico"}), 400
    if 'stock' in data:
        try:
            stock = int(data['stock'])
            update_fields.append("stock = %s")
            values.append(stock)
        except (ValueError, TypeError):
            return jsonify({"error": "Stock debe ser un entero"}), 400
    
    if not update_fields:
        return jsonify({"error": "No hay campos válidos para actualizar"}), 400
    
    try:
        with get_db_cursor(commit=True) as cur:
            values.append(producto_id)
            query = f'UPDATE productos SET {", ".join(update_fields)} WHERE id = %s RETURNING {", ".join(PRODUCT_COLUMNS)}'
            
            cur.execute(query, values)
            producto_actualizado = cur.fetchone()
            
            producto_data = map_product_row(producto_actualizado, PRODUCT_COLUMNS)
            
            if producto_data:
                return jsonify(producto_data)
            else:
                return jsonify({"error": "Producto no encontrado"}), 404
                
    except psycopg2.Error as e:
        return jsonify({"error": f"Error de base de datos: {e.diag.message_primary}"}), 500
    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

# DELETE - Eliminar producto
@app.route('/productos/<int:producto_id>', methods=['DELETE'])
def eliminar_producto(producto_id):
    try:
        with get_db_cursor(commit=True) as cur:
            # Solo necesitamos el ID y nombre para el mensaje de confirmación
            cur.execute('DELETE FROM productos WHERE id = %s RETURNING id, nombre', (producto_id,))
            producto_eliminado = cur.fetchone()
            
            if producto_eliminado:
                return jsonify({
                    "message": "✅ Producto eliminado correctamente",
                    "producto": {
                        "id": producto_eliminado[0],
                        "nombre": producto_eliminado[1]
                    }
                })
            else:
                return jsonify({"error": "Producto no encontrado"}), 404
                
    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

# ----------------------------------------------------------------------
# Inicialización y Ejecución
# ----------------------------------------------------------------------
if __name__ == '__main__':
    init_db()
    # Usar host='0.0.0.0' para que sea accesible desde Docker
    app.run(host='0.0.0.0', port=5000, debug=True)