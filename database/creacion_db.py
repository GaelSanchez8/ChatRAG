import sqlite3
import os

# Obtener la ruta de la base de datos de forma relativa (funciona en cualquier máquina)
db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'chatbot_rag.db')

# Crear la carpeta 'data' si no existe
os.makedirs(os.path.dirname(db_path), exist_ok=True)

conexion = sqlite3.connect(db_path)
cursor = conexion.cursor()

#Creación de la tabla para los usuarios.
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Usuarios (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Correo TEXT NOT NULL UNIQUE,
        Password_Hash TEXT NOT NULL
    )
''')


#Creación de la tabla para las conversaciones.
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Conversaciones (
        ID_Conversación INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_Usuario INTEGER NOT NULL,
        Nombre_Archivo TEXT NOT NULL,
        FOREIGN KEY (ID_Usuario) REFERENCES Usuarios(ID)
    )
''')


# Creación de la tabla para los mensajes.
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Mensajes (
        ID_Mensaje INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_Conversacion INTEGER NOT NULL,
        Emisor TEXT NOT NULL,
        Texto TEXT NOT NULL,
        Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (ID_Conversacion) REFERENCES Conversaciones(ID_Conversacion)
    )
''')

#Se guardan los cambios de la base de datos y se cierra la conexión.
conexion.commit()
conexion.close()
print("Base de datos creada exitosamente.")