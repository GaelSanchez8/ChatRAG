import re
import bcrypt

def validar_password(password):
    """"
    Evaluar que la contraseña cumpla con los requisitos 
    - Minimo 10 caracteres
    - Al menos un numero
    - Al menos un caracter especial
    """
    if len(password) < 10:
        return False, "La contraseña debe de tener al menos 10 caracteres."
    if not re.search(r'\d', password):
        return False, "La contraseña debe de contener al menos un número."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "La contraseña debe de contener al menos un caracter especial."
    return True, "Contraseña válida."


def encriptar_password(password_plana):
    """"
    Encriptar la contraseña utilizando bcrypt
    """
    password_bytes = password_plana.encode('utf-8')
    # gensalt() agrega texto aleatorio para hacer que el hash sea único incluso para contraseñas iguales
    salt = bcrypt.gensalt()
    # bcrypt.hashpw() hace el hash de la contraseña utilizando el salt generado
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)

    # Se regresa a texto normal para almacenarlo en la base de datos
    return hashed_bytes.decode('utf-8')


def verificar_login(password_ingresada, hash_almacenado):
    """"
    Verificar que la contraseña ingresada por el usuario coincida con el hash almacenado en la base de datos
    """
    password_bytes = password_ingresada.encode('utf-8')
    hash_bytes = hash_almacenado.encode('utf-8')

    return bcrypt.checkpw(password_bytes, hash_bytes)
