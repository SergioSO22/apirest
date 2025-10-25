from flask import Flask, jsonify, request, render_template, redirect, url_for
import psycopg2
import os
from datetime import datetime
from contextlib import contextmanager
# Importar dotenv
from dotenv import load_dotenv 

# Cargar variables de entorno desde el archivo .env
load_dotenv() 

app = Flask(__name__)

# --- Configuración de la base de datos ---
# Se recomienda usar Docker o variables de entorno para producción
DATABASE_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'database': os.environ.get('DB_NAME', 'crud_db'),
    'user': os.environ.get('DB_USER', 'postgres'),
    'password': os.environ.get('DB_PASSWORD', 'password'),
    'port': os.environ.get('DB_PORT', '5432')
}

# ----------------------------------------------------------------------
# 🌟 MEJORA: Manejo de Conexiones (Context Manager)
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
                ON CONFLICT DO NOTHING
            ''')
        print("Base de datos inicializada y tabla 'productos' creada. ✅")
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e} ❌")
        # Es crucial detener la aplicación si la DB no está lista
        exit(1)

# ----------------------------------------------------------------------
# 🌟 MEJORA: Abstracción de Datos (Función de mapeo)
# ----------------------------------------------------------------------

def map_product_row(row, columns):
    """Mapea una fila de la DB (tupla) a un diccionario de producto."""
    if not row:
        return None
    # Aseguramos la conversión de tipos para la salida JSON/HTML
    return {
        'id': row[0],
        'nombre': row[1],
        'precio': float(row[2]),
        'stock': row[3],
        'fecha_creacion': row[4].isoformat() if isinstance(row[4], datetime) else str(row[4])
    }

PRODUCT_COLUMNS = ['id', 'nombre', 'precio', 'stock', 'fecha_creacion']
SELECT_QUERY = f'SELECT {", ".join(PRODUCT_COLUMNS)} FROM productos'

# ----------------------------------------------------------------------
# ENDPOINTS DE INTERFAZ DE USUARIO (UI) - CRUD WEB
# ----------------------------------------------------------------------


@app.route('/')
def home():
    """
    Ruta raíz que ahora renderiza una página HTML de bienvenida
    en lugar de devolver JSON.
    """
    # Lista de endpoints para mostrar en la página de bienvenida (opcional)
    endpoints = {
        "UI CRUD Productos": url_for('ui_productos'),
        "API (JSON) /productos": url_for('obtener_productos')
    }
    # Renderiza la nueva plantilla 'welcome.html'
    return render_template('welcome.html', endpoints=endpoints)

@app.route('/ui/productos', methods=['GET', 'POST'])
def ui_productos():
    if request.method == 'POST':
        # --- Manejar la creación del producto (CREATE) ---
        nombre = request.form.get('nombre')
        precio_str = request.form.get('precio')
        stock_str = request.form.get('stock', '0')
        
        if not nombre or not precio_str:
            return redirect(url_for('ui_productos')) # Redirige si faltan datos
        
        try:
            precio = float(precio_str)
            stock = int(stock_str)
            
            with get_db_cursor(commit=True) as cur:
                cur.execute(
                    'INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)',
                    (nombre, precio, stock)
                )
            return redirect(url_for('ui_productos'))
        except (ValueError, psycopg2.Error) as e:
            return f"Error al crear producto: {e}", 500

    # --- Mostrar la lista de productos (READ) ---
    try:
        with get_db_cursor(commit=False) as cur:
            cur.execute(f'{SELECT_QUERY} ORDER BY id')
            productos_data = cur.fetchall()
            productos_list = [map_product_row(p, PRODUCT_COLUMNS) for p in productos_data]
            
            return render_template('productos.html', productos=productos_list)
    except Exception as e:
        return f"Error al cargar productos: {e}", 500

@app.route('/ui/productos/editar/<int:producto_id>', methods=['GET', 'POST'])
def ui_editar_producto(producto_id):
    if request.method == 'POST':
        # --- Manejar la actualización (UPDATE) ---
        nombre = request.form.get('nombre')
        precio_str = request.form.get('precio')
        stock_str = request.form.get('stock')
        
        update_fields = []
        values = []
        
        if nombre:
            update_fields.append("nombre = %s")
            values.append(nombre)
        if precio_str:
            try:
                values.append(float(precio_str))
                update_fields.append("precio = %s")
            except ValueError:
                return "Precio debe ser un número válido", 400
        if stock_str:
            try:
                values.append(int(stock_str))
                update_fields.append("stock = %s")
            except ValueError:
                return "Stock debe ser un entero válido", 400

        if not update_fields:
            return redirect(url_for('ui_productos'))

        try:
            with get_db_cursor(commit=True) as cur:
                values.append(producto_id)
                query = f'UPDATE productos SET {", ".join(update_fields)} WHERE id = %s'
                cur.execute(query, values)
                return redirect(url_for('ui_productos'))
        except (psycopg2.Error, Exception) as e:
            return f"Error al actualizar producto: {e}", 500
    
    # --- Mostrar el formulario de edición (GET) ---
    try:
        with get_db_cursor(commit=False) as cur:
            cur.execute(f'{SELECT_QUERY} WHERE id = %s', (producto_id,))
            producto = map_product_row(cur.fetchone(), PRODUCT_COLUMNS)
            
            if not producto:
                return "Producto no encontrado", 404
            
            # Cargamos todos los productos para que la tabla siga visible
            cur.execute(f'{SELECT_QUERY} ORDER BY id')
            productos_data = cur.fetchall()
            productos_list = [map_product_row(p, PRODUCT_COLUMNS) for p in productos_data]

            return render_template('productos.html', producto_a_editar=producto, productos=productos_list)
    except Exception as e:
        return f"Error al cargar producto para edición: {e}", 500

@app.route('/ui/productos/eliminar/<int:producto_id>', methods=['POST'])
def ui_eliminar_producto(producto_id):
    try:
        with get_db_cursor(commit=True) as cur:
            cur.execute('DELETE FROM productos WHERE id = %s', (producto_id,))
            # Redirige a la vista principal después de la eliminación
            return redirect(url_for('ui_productos'))
    except Exception as e:
        return f"Error al eliminar producto: {e}", 500


# ----------------------------------------------------------------------
# ENDPOINTS API (JSON) - Originales (Mantenidos para compatibilidad)
# ----------------------------------------------------------------------

# CREATE - Crear producto (JSON)
@app.route('/productos', methods=['POST'])
def crear_producto():
    data = request.get_json()
    nombre = data.get('nombre')
    precio = data.get('precio')
    stock = data.get('stock', 0)
    
    if not nombre or not precio:
        return jsonify({"error": "Nombre y precio son requeridos"}), 400
    
    try:
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
            
            producto_data = map_product_row(nuevo_producto, PRODUCT_COLUMNS)
            return jsonify(producto_data), 201
    
    except psycopg2.Error as e:
        return jsonify({"error": f"Error de base de datos: {e.diag.message_primary}"}), 500
    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

# READ - Obtener todos los productos (JSON, con paginación básica)
@app.route('/productos', methods=['GET'])
def obtener_productos():
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        offset = (page - 1) * limit
        
        sql = f"{SELECT_QUERY} ORDER BY id LIMIT %s OFFSET %s"
        
        with get_db_cursor(commit=False) as cur:
            cur.execute(sql, (limit, offset))
            productos = cur.fetchall()
            
            productos_list = [map_product_row(p, PRODUCT_COLUMNS) for p in productos]
            
            return jsonify(productos_list)
            
    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

# READ - Obtener producto por ID (JSON)
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

# UPDATE - Actualizar producto (JSON)
@app.route('/productos/<int:producto_id>', methods=['PUT'])
def actualizar_producto(producto_id):
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No hay datos para actualizar"}), 400
        
    update_fields = []
    values = []
    
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

# DELETE - Eliminar producto (JSON)
@app.route('/productos/<int:producto_id>', methods=['DELETE'])
def eliminar_producto(producto_id):
    try:
        with get_db_cursor(commit=True) as cur:
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