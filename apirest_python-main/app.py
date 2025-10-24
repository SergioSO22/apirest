from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3

app = Flask(__name__, static_folder='static')
CORS(app)  # Habilitar CORS para permitir peticiones desde el frontend

DB_PATH = 'personas.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS personas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            edad INTEGER NOT NULL,
            email TEXT,
            telefono TEXT,
            direccion TEXT,
            fecha_nacimiento TEXT,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

init_db()

# Endpoint para obtener todas las personas
@app.route('/personas', methods=['GET'])
def get_personas():
    try:
        conn = get_db_connection()
        personas = conn.execute('SELECT * FROM personas').fetchall()
        conn.close()

        lista_personas = []
        for persona in personas:
            lista_personas.append({
                'id': persona['id'],
                'nombre': persona['nombre'],
                'apellido': persona['apellido'],
                'edad': persona['edad'],
                'email': persona['email'],
                'telefono': persona['telefono'],
                'direccion': persona['direccion'],
                'fecha_nacimiento': persona['fecha_nacimiento'],
                'fecha_registro': persona['fecha_registro']
            })
        return jsonify({
            'success': True,
            'personas': lista_personas
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    
# Endpoint para crear una nueva persona
@app.route('/personas', methods=['POST'])
def create_persona():
    try:
        data = request.get_json()
        nombre = data['nombre']
        apellido = data['apellido']
        edad = data['edad']
        email = data.get('email', '')
        telefono = data.get('telefono', '')
        direccion = data.get('direccion', '')
        fecha_nacimiento = data.get('fecha_nacimiento', '')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO personas (nombre, apellido, edad, email, telefono, direccion, fecha_nacimiento)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (nombre, apellido, edad, email, telefono, direccion, fecha_nacimiento))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()

        return jsonify({
            'success': True,
            'persona': {
                'id': new_id,
                'nombre': nombre,
                'apellido': apellido,
                'edad': edad,
                'email': email,
                'telefono': telefono,
                'direccion': direccion,
                'fecha_nacimiento': fecha_nacimiento
            }
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    
# Endpoint para actualizar una persona existente
@app.route('/personas/<int:persona_id>', methods=['PUT'])
def update_persona(persona_id):
    try:
        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'error': 'No se proporcionaron datos para actualizar'}), 400

        conn = get_db_connection()
        persona = conn.execute('SELECT * FROM personas WHERE id = ?', (persona_id,)).fetchone()
        if persona is None:
            conn.close()
            return jsonify({'success': False, 'error': 'Persona no encontrada'}), 404

        nombre = data.get('nombre')
        apellido = data.get('apellido')
        edad = data.get('edad')
        email = data.get('email')
        telefono = data.get('telefono')
        direccion = data.get('direccion')
        fecha_nacimiento = data.get('fecha_nacimiento')

        conn.execute('''
            UPDATE personas
            SET nombre = ?, apellido = ?, edad = ?, email = ?, telefono = ?, direccion = ?, fecha_nacimiento = ?
            WHERE id = ?
        ''', (
            nombre if nombre is not None else persona['nombre'],
            apellido if apellido is not None else persona['apellido'],
            edad if edad is not None else persona['edad'],
            email if email is not None else persona['email'],
            telefono if telefono is not None else persona['telefono'],
            direccion if direccion is not None else persona['direccion'],
            fecha_nacimiento if fecha_nacimiento is not None else persona['fecha_nacimiento'],
            persona_id
        ))
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Persona actualizada correctamente'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    
# Endpoint para eliminar una persona
@app.route('/personas/<int:persona_id>', methods=['DELETE'])
def delete_persona(persona_id):
    try:
        conn = get_db_connection()
        persona = conn.execute('SELECT * FROM personas WHERE id = ?', (persona_id,)).fetchone()
        if persona is None:
            conn.close()
            return jsonify({'success': False, 'error': 'Persona no encontrada'}), 404

        conn.execute('DELETE FROM personas WHERE id = ?', (persona_id,))
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Persona eliminada correctamente'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Ruta para servir la interfaz gráfica
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    app.run(debug=True, port=4000)
