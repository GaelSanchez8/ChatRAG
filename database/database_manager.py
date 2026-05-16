import os
import psycopg2
from dotenv import load_dotenv
from src.logic import auth_manager


load_dotenv()  # Carga las variables de entorno desde el archivo .env

def obtener_conexion():
    # Estrablece la conexión a la base de datos utilizando las variables de entorno
    try:
        conexion = psycopg2.connect(
            host=os.getenv('SUPABASE_HOST'),
            port=os.getenv('SUPABASE_DB_PORT'),
            database=os.getenv('SUPABASE_DB_NAME'),
            user=os.getenv('SUPABASE_DB_USER'),
            password=os.getenv('SUPABASE_DB_PASSWORD')
        )
        return conexion
    except Exception as e:
        print(f" Error al conectar a la base de datos: {e}")
        return None
    

def inicializar_base_de_datos():
    #Crea las tablas necesarias en la nube si no existen 
    conexion = obtener_conexion()
    if not conexion:
        return
    
    try:
        cursor = conexion.cursor()

        # Crear tabla de usuarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                correo varchar(255) UNIQUE NOT NULL,
                password_hash varchar(255) NOT NULL,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        conexion.commit()
        print("Base de datos inicializada correctamente.")
    except Exception as e:
        print(f" Error al inicializar la base de datos: {e}")
    finally:
        cursor.close()
        conexion.close()


def registrar_usuario(correo, password_plana):
    # Recibe un correo y una contraseña plana, hashea la contraseña y la guarda en la base de datos
    conexion = obtener_conexion()
    if not conexion:
        return False
    
    cursor = None

    # Indica que no se pudo conectar a la base de datos
    try:
        hash_password = auth_manager.encriptar_password(password_plana) # Hashea la contraseña utilizando el auth_manager
        cursor = conexion.cursor()

        # Inserta el nuevo usuario en la base de datos 
        sql = "INSERT INTO usuarios (correo, password_hash) VALUES (%s, %s)"
        cursor.execute(sql, (correo, hash_password))
        conexion.commit()
        return True, "Usuario registrado exitosamente." 
    except psycopg2.errors.UniqueViolation: 
        # Lanzara el error si el correo ya existe en la base de datos
        conexion.rollback()
        return False, "El correo ya está registrado."
    except Exception as e:
        conexion.rollback()
        return False, f"Error al registrar el usuario: {e}"
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()


def validar_login(correo, password_plana):
    # Busca el correo, extrae el hash de la contraseña y lo compara con la contraseña plana utilizando el auth_manager

    conexion = obtener_conexion()
    if not conexion:
        return False, "Error de conexión a la base de datos."
    
    cursor = None

    try:
        cursor = conexion.cursor()
        #Busca el usuario por correo
        sql = "SELECT password_hash FROM usuarios WHERE correo = %s"
        cursor.execute(sql, (correo,))
        resultado = cursor.fetchone() #Trae la primera fila del resultado, que debería ser el hash de la contraseña

        if not resultado:
            return False, "Correo no encontrado."
        
        hash_guardado =  resultado[0]

        #Compara la contraseña plana con el hash utilizando el auth_manager
        if auth_manager.verificar_login(password_plana, hash_guardado):
            return True, "Login exitoso."
        else:
            return False, "Contraseña incorrecta."
    except Exception as e:
        return False, f"Error al validar el login: {e}"
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()


#Prueba de la base de datos
if __name__ == "__main__":
    print("Inicializando la base de datos...")
    inicializar_base_de_datos()

    print("\n Prueba de registro")
    # intento de registro de un nuevo usuario
    exito_reg, msg_reg = registrar_usuario("test@correo.com", "contraseña123*")
    print(f"Resultado: {msg_reg}  ")

    # intento de registro con el mismo correo para probar la restricción de unicidad
    print("\n Prueba de login")
    exito_log, msg_log = validar_login("test@correo.com", "contraseña123*")
    print(f"Intento correcto: {msg_log}  ")

    # intento de login con contraseña incorrecta
    print("\n Prueba de login con contraseña incorrecta")
    exito_falso, msg_falso = validar_login("test@correo.com", "contraseñaincorrecta")
    print(f"Intento incorrecto: {msg_falso}  ")