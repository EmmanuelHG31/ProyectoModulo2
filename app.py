from flask import Flask, request, jsonify
import sqlite3
import bcrypt
import datetime
import jwt
import re
import logging

app = Flask(__name__)

# ==========================================
# CONFIGURACIÓN DEL MOTOR DE LOGS (20%)
# Formato: [Fecha y Hora] | [Nivel] | [Mensaje]
# ==========================================
logging.basicConfig(
    filename='sistema.log',
    level=logging.DEBUG,
    format='[%(asctime)s] | [%(levelname)s] | [%(message)s]',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row 
    return conn

# ==========================================
# ENDPOINT 1: REGISTRO
# ==========================================
@app.route('/registro', methods=['POST'])
def registro():
    datos = request.get_json()
    email = datos.get('email')
    password = datos.get('password')
    role = datos.get('role', 'cliente')

    logging.debug(f"Petición de registro recibida para el correo: {email}")

    if not email or not password:
        logging.warning("Intento de registro fallido: Faltan campos obligatorios.")
        return jsonify({"error": "Faltan datos"}), 400

    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        logging.warning(f"Formato de email inválido detectado: {email}")
        return jsonify({"mensaje": "Formato de email inválido"}), 400

    if not (len(password) >= 8 and len(password) <= 10):
        logging.warning(f"Contraseña fuera de rango para el usuario: {email}")
        return jsonify({"mensaje": "La contraseña debe contener de 8 a 10 caracteres"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        usuario_existente = cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,)).fetchone()

        if usuario_existente:
            logging.warning(f"Registro denegado: El usuario {email} ya existe.")
            conn.close()
            return jsonify({"mensaje": "El usuario ya existe"}), 409

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        cursor.execute('INSERT INTO usuarios (email, password, role) VALUES (?, ?, ?)', 
                       (email, hashed_password, role))
        conn.commit()
        conn.close()

        logging.info(f"Usuario registrado con éxito: {email}")
        return jsonify({"mensaje": "Usuario Registrado"}), 201

    except Exception as e:
        logging.error(f"Error crítico en base de datos al registrar {email}: {str(e)}")
        return jsonify({"error": "Error interno"}), 500

# ==========================================
# ENDPOINT 2: LOGIN (Core)
# ==========================================
@app.route('/login', methods=['POST'])
def login():
    datos = request.get_json()
    email = datos.get('email')
    password = datos.get('password')

    logging.debug(f"Intento de login para: {email}")

    if not email or not password:
        return jsonify({"error": "Faltan datos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    usuario = cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,)).fetchone()
    conn.close()

    if not usuario:
        logging.warning(f"Login fallido: Usuario {email} no encontrado.")
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    if bcrypt.checkpw(password.encode('utf-8'), usuario['password']):
        payload = {
            "id": usuario["id"],
            "role": usuario["role"],
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }
        token = jwt.encode(payload, "todopoderoso", algorithm="HS256")

        logging.info(f"Login exitoso para el usuario: {email}")
        return jsonify({"mensaje": "Login exitoso", "token": token}), 200
    else:
        logging.warning(f"Credenciales inválidas para el usuario: {email}")
        return jsonify({"mensaje": "Credenciales Invalidas"}), 401

# ==========================================
# ENDPOINT 3: MANTENIMIENTOS (Proceso de Negocio)
# ==========================================
@app.route('/mantenimientos', methods=['POST'])
def registrar_mantenimiento():
    datos = request.get_json()
    placa = datos.get('placa')
    descripcion = datos.get('descripcion')
    costo = datos.get('costo')
    fecha = datos.get('fecha')

    logging.debug(f"Intentando registrar mantenimiento para placa: {placa}")

    if not all([placa, descripcion, costo, fecha]):
        logging.warning(f"Mantenimiento incompleto para placa {placa}")
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    try:
        if float(costo) < 0:
            logging.warning(f"Costo negativo detectado ({costo}) para la placa {placa}")
            return jsonify({"error": "El costo no puede ser un valor negativo"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO mantenimientos (placa, descripcion, costo, fecha)
            VALUES (?, ?, ?, ?)
        ''', (placa, descripcion, costo, fecha))
        
        conn.commit()
        conn.close()
        
        logging.info(f"Mantenimiento guardado correctamente para la placa: {placa}")
        return jsonify({"mensaje": "Mantenimiento registrado con éxito"}), 201
    except Exception as e:
        logging.error(f"Falla de sistema al registrar mantenimiento de placa {placa}: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)