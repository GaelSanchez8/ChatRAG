import re
import bcrypt
import smtplib
from email.mime.text import MIMEText
import os
import random
import string

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


def enviar_email(correo_destino):
    """"
    Envia un correo real si las credenciales están en el .env, sino solo simula el envío mostrando un mensaje en la consola
    """
    remitente = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASSWORD")

    if not remitente or not password:
        print(f"\n[SIMULACIÓN SMTP]  Correo de bienvenida 'enviado' a: {correo_destino}")
        print("[SIMULACIÓN SMTP] Para enviar correos reales, configura EMAIL_REMITENTE y EMAIL_PASSWORD en tu archivo .env\n")
        return True
    
    try:
        texto = (
            "¡Hola!\n\n"
            "Tu cuenta en el Asistente IA de Cuervos Negros Salvajes ha sido creada con éxito.\n"
            "Ya puedes iniciar sesión en la aplicación de escritorio y comenzar a analizar tus documentos.\n\n"
            "Saludos,\nEl equipo de Cuervos Negros.")
        
        mensaje = MIMEText(texto)
        mensaje['Subject'] = 'Confirmación de Registro - Cuervos Negros Salvajes'
        mensaje['From'] = remitente
        mensaje['To'] = correo_destino

        #Conexion con el servidor de gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() #Encripta la conexion 
        server.login(remitente, password)
        server.send_message(mensaje)
        server.quit()
        
        print(f"[SMTP] Correo de bienvenida 'enviado' a: {correo_destino}")
        return True
    except Exception as e:
        print(f"[SMTP] Error al enviar correo: {e}")
        return False


def generar_codigo_verificacion():
    """Genera un código de 6 dígitos aleatorio para verificación de email"""
    return ''.join(random.choices(string.digits, k=6))


def enviar_codigo_verificacion(correo_destino, codigo_verificacion):
    """Envía el código de verificación por email"""
    remitente = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASSWORD")

    if not remitente or not password:
        print(f"\n[SIMULACIÓN SMTP] Código de verificación 'enviado' a: {correo_destino}")
        print(f"[SIMULACIÓN SMTP] Código: {codigo_verificacion}")
        print("[SIMULACIÓN SMTP] Válido por 20 minutos. Máximo 5 intentos.\n")
        return True
    
    try:
        texto = (
            f"¡Hola!\n\n"
            f"Tu código de verificación es: {codigo_verificacion}\n\n"
            f"Este código es válido por 20 minutos.\n"
            f"Tienes un máximo de 5 intentos para verificarlo.\n\n"
            f"Si no solicitaste este código, ignora este correo.\n\n"
            f"Saludos,\nEl equipo de Cuervos Negros.")
        
        mensaje = MIMEText(texto)
        mensaje['Subject'] = 'Código de Verificación - Cuervos Negros Salvajes'
        mensaje['From'] = remitente
        mensaje['To'] = correo_destino

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remitente, password)
        server.send_message(mensaje)
        server.quit()
        
        print(f"[SMTP] Código de verificación 'enviado' a: {correo_destino}")
        return True
    except Exception as e:
        print(f"[SMTP] Error al enviar código de verificación: {e}")
        return False