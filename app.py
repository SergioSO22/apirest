from flask import Flask, jsonify, request
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)

# Configuración de la base de datos
DATABASE_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'database': os.environ.get('DB_NAME', 'crud_db'),
    'user': os.environ.get('DB_USER', 'postgres'),
    'password': os.environ.get('DB_PASSWORD', 'password'),
    'port': os.environ.get('DB_PORT', '5432')
}

def get_db_connection():
    return psycopg2.connect(**DATABASE_CONFIG)

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
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
    
    conn.commit()
    cur.close()
    conn.close()

@app.route('/')
def home():
    return jsonify({
        "message": "API CRUD Python + PostgreSQL",
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
    try:
        data = request.get_json()
        
        if not data or not data.get('nombre') or not data.get('precio'):
            return jsonify({"error": "Nombre y precio son requeridos"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            'INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s) RETURNING id, nombre, precio, stock, fecha_creacion',
            (data['nombre'], float(data['precio']), data.get('stock', 0))
        )
        
        nuevo_producto = cur.fetchone()
        conn.commit()
        
        producto = {
            'id': nuevo_producto[0],
            'nombre': nuevo_producto[1],
            'precio': float(nuevo_producto[2]),
            'stock': nuevo_producto[3],
            'fecha_creacion': nuevo_producto[4]
        }
        
        cur.close()
        conn.close()
        return jsonify(producto), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# READ - Obtener todos los productos
@app.route('/productos', methods=['GET'])
def obtener_productos():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, nombre, precio, stock, fecha_creacion FROM productos ORDER BY id')
        productos = cur.fetchall()
        
        productos_list = []
        for producto in productos:
            productos_list.append({
                'id': producto[0],
                'nombre': producto[1],
                'precio': float(producto[2]),
                'stock': producto[3],
                'fecha_creacion': producto[4]
            })
        
        cur.close()
        conn.close()
        return jsonify(productos_list)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# READ - Obtener producto por ID
@app.route('/productos/<int:producto_id>', methods=['GET'])
def obtener_producto(producto_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, nombre, precio, stock, fecha_creacion FROM productos WHERE id = %s', (producto_id,))
        producto = cur.fetchone()
        
        if producto:
            producto_data = {
                'id': producto[0],
                'nombre': producto[1],
                'precio': float(producto[2]),
                'stock': producto[3],
                'fecha_creacion': producto[4]
            }
            cur.close()
            conn.close()
            return jsonify(producto_data)
        else:
            cur.close()
            conn.close()
            return jsonify({"error": "Producto no encontrado"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# UPDATE - Actualizar producto
@app.route('/productos/<int:producto_id>', methods=['PUT'])
def actualizar_producto(producto_id):
    try:
        data = request.get_json()
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Verificar si el producto existe
        cur.execute('SELECT id FROM productos WHERE id = %s', (producto_id,))
        if not cur.fetchone():
            cur.close()
            conn.close()
            return jsonify({"error": "Producto no encontrado"}), 404
        
        # Construir query dinámico
        update_fields = []
        values = []
        
        if 'nombre' in data:
            update_fields.append("nombre = %s")
            values.append(data['nombre'])
        if 'precio' in data:
            update_fields.append("precio = %s")
            values.append(float(data['precio']))
        if 'stock' in data:
            update_fields.append("stock = %s")
            values.append(data['stock'])
        
        if not update_fields:
            return jsonify({"error": "No hay campos para actualizar"}), 400
        
        values.append(producto_id)
        query = f'UPDATE productos SET {", ".join(update_fields)} WHERE id = %s RETURNING id, nombre, precio, stock, fecha_creacion'
        
        cur.execute(query, values)
        producto_actualizado = cur.fetchone()
        conn.commit()
        
        producto = {
            'id': producto_actualizado[0],
            'nombre': producto_actualizado[1],
            'precio': float(producto_actualizado[2]),
            'stock': producto_actualizado[3],
            'fecha_creacion': producto_actualizado[4]
        }
        
        cur.close()
        conn.close()
        return jsonify(producto)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# DELETE - Eliminar producto
@app.route('/productos/<int:producto_id>', methods=['DELETE'])
def eliminar_producto(producto_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute('DELETE FROM productos WHERE id = %s RETURNING id, nombre', (producto_id,))
        producto_eliminado = cur.fetchone()
        
        if producto_eliminado:
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({
                "message": "Producto eliminado correctamente",
                "producto": {
                    "id": producto_eliminado[0],
                    "nombre": producto_eliminado[1]
                }
            })
        else:
            conn.rollback()
            cur.close()
            conn.close()
            return jsonify({"error": "Producto no encontrado"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
