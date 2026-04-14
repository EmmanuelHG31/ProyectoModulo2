import sqlite3

def crear_base_de_datos():
    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()

    # 1. Eliminamos las tablas si existen para evitar errores al reiniciar
    cursor.execute("DROP TABLE IF EXISTS usuarios")
    cursor.execute("DROP TABLE IF EXISTS mantenimientos")

    # 2. Tabla de Usuarios (Para Registro y Login)
    sql_usuarios = """
    CREATE TABLE usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """

    # 3. Tabla de Mantenimientos (Tu nuevo módulo)
    sql_mantenimientos = """
    CREATE TABLE mantenimientos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        placa TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        costo REAL NOT NULL,
        fecha TEXT NOT NULL
    )
    """

    # Ejecutamos ambas sentencias
    cursor.execute(sql_usuarios)
    cursor.execute(sql_mantenimientos)
    
    conexion.commit()
    conexion.close()
    print("✅ Base de datos actualizada: Tablas 'usuarios' y 'mantenimientos' listas.")

if __name__ == "__main__":
    crear_base_de_datos()