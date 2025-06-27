from flask import Blueprint, request, jsonify, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

api = Blueprint('api', __name__)
DATABASE = 'tareas.db'

@api.route('/registro', methods=['POST'])
def registro():
    data = request.get_json()
    usuario = data.get('usuario')
    contraseña = data.get('contraseña')

    if not usuario or not contraseña:
        return jsonify({'error': 'Faltan datos'}), 400

    hash_contraseña = generate_password_hash(contraseña)
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO usuarios (usuario, contraseña) VALUES (?, ?)', (usuario, hash_contraseña))
            conn.commit()
        return jsonify({'mensaje': 'Usuario registrado correctamente'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Usuario ya existe'}), 409

@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = data.get('usuario')
    contraseña = data.get('contraseña')

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT contraseña FROM usuarios WHERE usuario = ?', (usuario,))
        result = cursor.fetchone()

        if result and check_password_hash(result[0], contraseña):
            return jsonify({'mensaje': 'Login exitoso'}), 200
        else:
            return jsonify({'error': 'Credenciales inválidas'}), 401

@api.route('/tareas', methods=['GET'])
def tareas():
    usuario = request.args.get('usuario')
    html = '''
    <html>
        <head><title>Bienvenido</title></head>
        <body>
            <h1>¡Bienvenido al sistema de tareas!</h1>
    '''

    if usuario:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, descripcion FROM tareas WHERE usuario = ?', (usuario,))
            tareas = cursor.fetchall()
            if tareas:
                html += "<h2>Tus tareas:</h2><ul>"
                for tid, desc in tareas:
                    html += f"<li><strong>ID {tid}:</strong> {desc}</li>"
                html += "</ul>"
            else:
                html += "<p>No tienes tareas registradas.</p>"

    html += "</body></html>"
    return render_template_string(html)

@api.route('/agregar_tarea', methods=['POST'])
def agregar_tarea():
    data = request.get_json()
    usuario = data.get('usuario')
    descripcion = data.get('descripcion')

    if not usuario or not descripcion:
        return jsonify({'error': 'Faltan datos'}), 400

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tareas (usuario, descripcion) VALUES (?, ?)', (usuario, descripcion))
        conn.commit()
    return jsonify({'mensaje': 'Tarea agregada correctamente'}), 201

@api.route('/eliminar_tarea', methods=['POST'])
def eliminar_tarea():
    data = request.get_json()
    tarea_id = data.get('id')

    if not tarea_id:
        return jsonify({'error': 'Falta el ID de la tarea'}), 400

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tareas WHERE id = ?', (tarea_id,))
        conn.commit()
    return jsonify({'mensaje': 'Tarea eliminada correctamente'}), 200
