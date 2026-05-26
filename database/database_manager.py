import os
import sqlite3
import psycopg2
from dotenv import load_dotenv
from datetime import datetime
from src.logic import auth_manager

load_dotenv()

# Variable global para controlar qué BD estamos usando
usar_sqlite = False
RUTA_SQLITE = "app_data.db"

def obtener_conexion():
    """Intenta conectar a Supabase primero, si falla usa SQLite"""
    global usar_sqlite
    
    # Si ya sabemos que Supabase no funciona, usa SQLite directamente
    if usar_sqlite:
        return obtener_conexion_sqlite()
    
    # Intenta conectar a Supabase con un límite de tiempo (Timeout)
    try:
        conexion = psycopg2.connect(
            host=os.getenv('SUPABASE_HOST'),
            port=os.getenv('SUPABASE_DB_PORT'),
            database=os.getenv('SUPABASE_DB_NAME'),
            user=os.getenv('SUPABASE_DB_USER'),
            password=os.getenv('SUPABASE_DB_PASSWORD'),
            connect_timeout=3  
        )
        print("✓ Conectado a Supabase (PostgreSQL)")
        return conexion
    except Exception as e:
        print(f"✗ Error al conectar a Supabase (Timeout o Red): {e}")
        print("↻ Cambiando automáticamente a SQLite (Modo Offline)...")
        usar_sqlite = True
        return obtener_conexion_sqlite()


def obtener_conexion_sqlite():
    """Conecta a la BD SQLite local"""
    try:
        conexion = sqlite3.connect(RUTA_SQLITE)
        conexion.row_factory = sqlite3.Row
        return conexion
    except Exception as e:
        print(f"Error al conectar a SQLite: {e}")
        return None
    

def inicializar_base_de_datos():
    """Crea las tablas necesarias (Supabase o SQLite según disponibilidad)"""
    conexion = obtener_conexion()
    if not conexion:
        print("No se pudo conectar a la base de datos. La aplicación continuará funcionando sin BD.")
        return
    
    cursor = None
    try:
        cursor = conexion.cursor()

        if usar_sqlite:
            # SQL para SQLite
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    correo TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    codigo_verificacion VARCHAR(6),
                    intentos_verificacion INTEGER DEFAULT 0,
                    fecha_codigo_generado TIMESTAMP,
                    verificado BOOLEAN DEFAULT 0,
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversaciones (
                    id_conversacion INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_usuario INTEGER NOT NULL,
                    nombre_archivo TEXT NOT NULL,
                    FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS mensajes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_conversacion INTEGER NOT NULL,
                    remitente VARCHAR(50) NOT NULL,
                    mensaje TEXT,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_conversacion) REFERENCES conversaciones(id_conversacion)
                );
            """)
        else:
            # SQL para PostgreSQL/Supabase
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id SERIAL PRIMARY KEY,
                    correo varchar(255) UNIQUE NOT NULL,
                    password_hash varchar(255) NOT NULL,
                    codigo_verificacion VARCHAR(6),
                    intentos_verificacion INTEGER DEFAULT 0,
                    fecha_codigo_generado TIMESTAMP,
                    verificado BOOLEAN DEFAULT FALSE,
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversaciones (
                    id_conversacion SERIAL PRIMARY KEY,
                    id_usuario INTEGER NOT NULL,
                    nombre_archivo TEXT NOT NULL,
                    FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS mensajes (
                    id SERIAL PRIMARY KEY,
                    id_conversacion INTEGER NOT NULL,
                    remitente VARCHAR(50) NOT NULL,
                    mensaje TEXT,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_conversacion) REFERENCES conversaciones(id_conversacion)
                );
            """)

        conexion.commit()
        modo = "SQLite (modo offline local)" if usar_sqlite else "Supabase (PostgreSQL en la nube)"
        print(f"✓ Base de datos inicializada correctamente en {modo}")
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()
    
    # Agregar columnas de verificación si no existen
    agregar_columnas_verificacion()


def agregar_columnas_verificacion():
    """Agrega las columnas de verificación a la tabla usuarios si no existen"""
    conexion = obtener_conexion()
    if not conexion:
        return
    
    cursor = None
    try:
        cursor = conexion.cursor()
        
        if usar_sqlite:
            # SQLite - agregar columnas si no existen
            cursor.execute("PRAGMA table_info(usuarios)")
            columnas = [col[1] for col in cursor.fetchall()]
            
            if "codigo_verificacion" not in columnas:
                cursor.execute("ALTER TABLE usuarios ADD COLUMN codigo_verificacion VARCHAR(6)")
            if "intentos_verificacion" not in columnas:
                cursor.execute("ALTER TABLE usuarios ADD COLUMN intentos_verificacion INTEGER DEFAULT 0")
            if "fecha_codigo_generado" not in columnas:
                cursor.execute("ALTER TABLE usuarios ADD COLUMN fecha_codigo_generado TIMESTAMP")
            if "verificado" not in columnas:
                cursor.execute("ALTER TABLE usuarios ADD COLUMN verificado BOOLEAN DEFAULT 0")
        else:
            # PostgreSQL - agregar columnas si no existen
            cursor.execute("""
                SELECT column_name FROM information_schema.columns 
                WHERE table_name='usuarios'
            """)
            columnas = [col[0] for col in cursor.fetchall()]
            
            if "codigo_verificacion" not in columnas:
                cursor.execute("ALTER TABLE usuarios ADD COLUMN codigo_verificacion VARCHAR(6)")
            if "intentos_verificacion" not in columnas:
                cursor.execute("ALTER TABLE usuarios ADD COLUMN intentos_verificacion INTEGER DEFAULT 0")
            if "fecha_codigo_generado" not in columnas:
                cursor.execute("ALTER TABLE usuarios ADD COLUMN fecha_codigo_generado TIMESTAMP")
            if "verificado" not in columnas:
                cursor.execute("ALTER TABLE usuarios ADD COLUMN verificado BOOLEAN DEFAULT FALSE")
        
        conexion.commit()
        print("✓ Columnas de verificación agregadas correctamente")
    except Exception as e:
        # Las columnas ya existen, ignorar el error
        if "already exists" not in str(e) and "duplicate" not in str(e).lower():
            print(f"Info: {e}")
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()


def registrar_usuario(correo, password_plana):
    """Registra un nuevo usuario (funciona con ambas BDs)"""
    es_valida, mensaje_validacion = auth_manager.validar_password(password_plana)
    if not es_valida:
        return False, mensaje_validacion
    
    conexion = obtener_conexion()
    if not conexion:
        return False, "Error de conexión a la base de datos."
    
    cursor = None
    try:
        hash_password = auth_manager.encriptar_password(password_plana)
        codigo_verificacion = auth_manager.generar_codigo_verificacion()
        fecha_codigo = datetime.now()
        
        cursor = conexion.cursor()

        sql = "INSERT INTO usuarios (correo, password_hash, codigo_verificacion, fecha_codigo_generado, intentos_verificacion) VALUES (?, ?, ?, ?, ?)" if usar_sqlite else "INSERT INTO usuarios (correo, password_hash, codigo_verificacion, fecha_codigo_generado, intentos_verificacion) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (correo, hash_password, codigo_verificacion, fecha_codigo, 0))
        conexion.commit()
        
        # Enviar código de verificación por email
        auth_manager.enviar_codigo_verificacion(correo, codigo_verificacion)
        
        return True, "Usuario registrado. Revisa tu correo para obtener el código de verificación."
    except sqlite3.IntegrityError if usar_sqlite else psycopg2.errors.UniqueViolation:
        conexion.rollback()
        return False, "El correo ya está registrado."
    except Exception as e:
        conexion.rollback()
        return False, f"Error al registrar el usuario: {e}"
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()


def validar_login(correo, password_plana):
    """Valida el login (funciona con ambas BDs)"""
    conexion = obtener_conexion()
    if not conexion:
        return False, "Error de conexión a la base de datos.", None
    
    cursor = None
    try:
        cursor = conexion.cursor()
        sql = "SELECT id, password_hash, verificado FROM usuarios WHERE correo = ?" if usar_sqlite else "SELECT id, password_hash, verificado FROM usuarios WHERE correo = %s"
        cursor.execute(sql, (correo,))
        resultado = cursor.fetchone()

        if not resultado:
            return False, "Correo no encontrado.", None
        
        id_usuario = resultado[0] 
        hash_guardado = resultado[1]
        verificado = resultado[2] if len(resultado) > 2 else False

        # Verificar que el email esté verificado
        if not verificado:
            return False, "Debes verificar tu email para poder acceder. Revisa tu bandeja de entrada.", None

        if auth_manager.verificar_login(password_plana, hash_guardado):
            return True, "Login exitoso.", id_usuario
        else:
            return False, "Contraseña incorrecta.", None
    except Exception as e:
        return False, f"Error al validar el login: {e}", None
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()


def insertar_mensaje_db(id_conversacion, remitente, texto_mensaje):
    """Inserta un mensaje en la conversación"""
    conexion = obtener_conexion()
    if not conexion:
        print("Error de conexión a la base de datos.")
        return False
    cursor = None
    try:
        cursor = conexion.cursor()
        sql = "INSERT INTO mensajes (id_conversacion, remitente, mensaje) VALUES (?, ?, ?)" if usar_sqlite else "INSERT INTO mensajes (id_conversacion, remitente, mensaje) VALUES (%s, %s, %s)"
        cursor.execute(sql, (id_conversacion, remitente, texto_mensaje))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al insertar el mensaje: {e}")
        if conexion:
            conexion.rollback()
        return False
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()


def crear_conversacion_db(id_usuario, nombre_archivo):
    """Crea una nueva conversación"""
    conexion = obtener_conexion()
    if not conexion:
        print("Error de conexión a la base de datos.")
        return None
    cursor = None
    try:
        cursor = conexion.cursor()
        sql = "INSERT INTO conversaciones (id_usuario, nombre_archivo) VALUES (?, ?)" if usar_sqlite else "INSERT INTO conversaciones (id_usuario, nombre_archivo) VALUES (%s, %s) RETURNING id_conversacion"
        cursor.execute(sql, (id_usuario, nombre_archivo))
        
        if usar_sqlite:
            id_conversacion = cursor.lastrowid
        else:
            id_conversacion = cursor.fetchone()[0]
            
        conexion.commit()
        return id_conversacion
    except Exception as e:
        print(f"Error al crear la conversación: {e}")
        if conexion:
            conexion.rollback()
        return None
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()


def obtener_conversacion_por_archivo(id_usuario, nombre_archivo):
    """Obtiene la conversación para un archivo específico"""
    conexion = obtener_conexion()
    if not conexion:
        return None
    cursor = None
    try:
        cursor = conexion.cursor()
        sql = "SELECT id_conversacion FROM conversaciones WHERE id_usuario = ? AND nombre_archivo = ? LIMIT 1" if usar_sqlite else "SELECT id_conversacion FROM conversaciones WHERE id_usuario = %s AND nombre_archivo = %s LIMIT 1"
        cursor.execute(sql, (id_usuario, nombre_archivo))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None
    except Exception as e:
        print(f"Error al obtener la conversación: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()


def obtener_mensajes_db(id_conversacion):
    """Obtiene todos los mensajes de una conversación"""
    conexion = obtener_conexion()
    if not conexion:
        return []
    
    cursor = None
    try:
        cursor = conexion.cursor()
        sql = "SELECT remitente, mensaje, fecha FROM mensajes WHERE id_conversacion = ? ORDER BY fecha ASC" if usar_sqlite else "SELECT remitente, mensaje, fecha FROM mensajes WHERE id_conversacion = %s ORDER BY fecha ASC"
        cursor.execute(sql, (id_conversacion,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener los mensajes: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()


def obtener_correo_por_id(id_usuario):
    """Obtiene el correo del usuario basado en su ID"""
    conexion = obtener_conexion()
    if not conexion:
        return None
    cursor = None
    try:
        cursor = conexion.cursor()
        sql = "SELECT correo FROM usuarios WHERE id = ?" if usar_sqlite else "SELECT correo FROM usuarios WHERE id = %s"
        cursor.execute(sql, (id_usuario,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None
    except Exception as e:
        print(f"Error al obtener el correo del usuario: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()


def verificar_codigo(correo, codigo_ingresado):
    """Verifica el código de verificación del usuario"""
    conexion = obtener_conexion()
    if not conexion:
        return False, "Error de conexión a la base de datos."
    
    cursor = None
    try:
        cursor = conexion.cursor()
        sql = "SELECT codigo_verificacion, fecha_codigo_generado, intentos_verificacion FROM usuarios WHERE correo = ?" if usar_sqlite else "SELECT codigo_verificacion, fecha_codigo_generado, intentos_verificacion FROM usuarios WHERE correo = %s"
        cursor.execute(sql, (correo,))
        resultado = cursor.fetchone()
        
        if not resultado:
            return False, "Usuario no encontrado."
        
        codigo_guardado, fecha_codigo, intentos = resultado
        
        # Verificar si ya está verificado
        sql_verificado = "SELECT verificado FROM usuarios WHERE correo = ?" if usar_sqlite else "SELECT verificado FROM usuarios WHERE correo = %s"
        cursor.execute(sql_verificado, (correo,))
        verificado = cursor.fetchone()[0]
        
        if verificado:
            return False, "Este usuario ya ha sido verificado."
        
        # Verificar intentos
        if intentos >= 5:
            return False, "Máximo de intentos alcanzado. Solicita un nuevo código."
        
        # Verificar expiración (20 minutos)
        from datetime import timedelta

        if isinstance(fecha_codigo, str):
            fecha_codigo = datetime.strptime(fecha_codigo.split(".")[0], "%Y-%m-%d %H:%M:%S")
            
        tiempo_transcurrido = datetime.now() - fecha_codigo
        if tiempo_transcurrido > timedelta(minutes=20):
            return False, "El código ha expirado. Solicita un nuevo código."
        
        # Verificar código
        if codigo_ingresado != codigo_guardado:
            # Incrementar intentos
            nuevo_intento = intentos + 1
            sql_update = "UPDATE usuarios SET intentos_verificacion = ? WHERE correo = ?" if usar_sqlite else "UPDATE usuarios SET intentos_verificacion = %s WHERE correo = %s"
            cursor.execute(sql_update, (nuevo_intento, correo))
            conexion.commit()
            
            intentos_restantes = 5 - nuevo_intento
            return False, f"Código incorrecto. Intentos restantes: {intentos_restantes}"
        
        # Código correcto - marcar como verificado
        sql_verify = "UPDATE usuarios SET verificado = 1, codigo_verificacion = NULL WHERE correo = ?" if usar_sqlite else "UPDATE usuarios SET verificado = TRUE, codigo_verificacion = NULL WHERE correo = %s"
        cursor.execute(sql_verify, (correo,))
        conexion.commit()
        
        return True, "Email verificado correctamente. Ya puedes usar el chatbot."
    except Exception as e:
        return False, f"Error al verificar el código: {e}"
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()


def reenviar_codigo(correo):
    """Reenvía un nuevo código de verificación al usuario"""
    conexion = obtener_conexion()
    if not conexion:
        return False, "Error de conexión a la base de datos."
    
    cursor = None
    try:
        # Generar nuevo código
        nuevo_codigo = auth_manager.generar_codigo_verificacion()
        fecha_codigo = datetime.now()
        
        cursor = conexion.cursor()
        
        # Actualizar código en BD y reiniciar intentos
        sql = "UPDATE usuarios SET codigo_verificacion = ?, fecha_codigo_generado = ?, intentos_verificacion = 0 WHERE correo = ?" if usar_sqlite else "UPDATE usuarios SET codigo_verificacion = %s, fecha_codigo_generado = %s, intentos_verificacion = 0 WHERE correo = %s"
        cursor.execute(sql, (nuevo_codigo, fecha_codigo, correo))
        conexion.commit()
        
        # Enviar nuevo código
        auth_manager.enviar_codigo_verificacion(correo, nuevo_codigo)
        
        return True, "Nuevo código enviado a tu correo."
    except Exception as e:
        return False, f"Error al reenviar el código: {e}"
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()


def obtener_id_por_correo(correo):
    """Obtiene el ID del usuario por su correo"""
    conexion = obtener_conexion()
    if not conexion:
        return None
    
    cursor = None
    try:
        cursor = conexion.cursor()
        sql = "SELECT id FROM usuarios WHERE correo = ?" if usar_sqlite else "SELECT id FROM usuarios WHERE correo = %s"
        cursor.execute(sql, (correo,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None
    except Exception as e:
        print(f"Error al obtener ID del usuario: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()


def obtener_datos_completos_conversacion(id_conversacion):

    """Obtiene todos los datos de una conversación"""
    conexion = obtener_conexion()
    if not conexion:
        return None
    cursor = None
    try:
        cursor = conexion.cursor()
        sql = "SELECT nombre_archivo FROM conversaciones WHERE id_conversacion = ?" if usar_sqlite else "SELECT nombre_archivo FROM conversaciones WHERE id_conversacion = %s"
        cursor.execute(sql, (id_conversacion,))
        res = cursor.fetchone()
        if not res:
            return None
        nombre_archivo = res[0]
        
        sql = "SELECT remitente, mensaje, fecha FROM mensajes WHERE id_conversacion = ? ORDER BY id ASC" if usar_sqlite else "SELECT remitente, mensaje, fecha FROM mensajes WHERE id_conversacion = %s ORDER BY id ASC"
        cursor.execute(sql, (id_conversacion,))
        filas = cursor.fetchall()

        mensajes_lista = []
        for fila in filas:
            # Esta línea que armaste soluciona perfectamente la diferencia de fechas entre SQLite y Postgres
            fecha_str = str(fila[2]) if fila[2] else "Sin fecha"
            mensajes_lista.append({"remitente": fila[0], "contenido": fila[1], "fecha": fecha_str})
        return {"id_conversacion": id_conversacion, 
                "nombre_archivo": nombre_archivo, 
                "mensajes": mensajes_lista}
    
    except Exception as e:
        print(f"Error al obtener datos de la conversación: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()