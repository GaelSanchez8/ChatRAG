import fitz  # PyMuPDF
import os
from google import genai
from dotenv import load_dotenv
import math
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    cliente = genai.Client(api_key=API_KEY)
else:
    cliente = None


def extraer_texto_pdf(ruta_archivo):
    texto_completo = ""
    # Abre un archivo PDF, lee su contenido y lo devuelve como texto
    try:
        documento = fitz.open(ruta_archivo)
        for numero_pagina in range(documento.page_count):
            pagina = documento.load_page(numero_pagina)
            texto_completo += pagina.get_text()
        documento.close()

        print(f"Se extrayó el texto del PDF: {ruta_archivo}")
        return texto_completo
    except Exception as e:
        print(f"Error al extraer texto del PDF: {e}")
        return None


def dividir_texto_en_chunks(texto, tamaño_chunk=1000, solapamiento=200):
    # Divide el texto en partes más pequeñas (chunks) para facilitar su procesamiento, respetando parrafos para no hacer cortes abruptos
    parrafos = texto.split("\n\n")  # Dividir el texto en párrafos
    chunks = []
    chunk_actual = ""

    for parrafo in parrafos:
        parrafo = parrafo.strip()
        if not parrafo:
            continue

        # Si el párrafo actual más el nuevo párrafo exceden el tamaño del chunk, guardar el chunk actual y empezar uno nuevo
        if len(chunk_actual) + len(parrafo) > tamaño_chunk and chunk_actual:
            chunks.append(chunk_actual.strip())
            chunk_actual = parrafo + " "  # Empezar un nuevo chunk con el párrafo actual
        else:
            chunk_actual += parrafo + " "  # Agregar el párrafo al chunk actual
    
    if chunk_actual:  # Agregar el último chunk si no está vacío
        chunks.append(chunk_actual.strip())
    
    return chunks


#Motor de busqueda semantica (embeddings) para encontrar el chunk más relevante para la pregunta que se haga y devolver ese chunk para que la IA lo procese
def calcular_similitud_coseno(vec1, vec2):
    # Calcula la similitud coseno entre dos vectores
    producto_punto = sum(a * b for a, b in zip(vec1, vec2))
    magnitud_vec1 = math.sqrt(sum(a * a for a in vec1))
    magnitud_vec2 = math.sqrt(sum(b * b for b in vec2))

    if magnitud_vec1 == 0 or magnitud_vec2 == 0:
        return 0.0
    return producto_punto / (magnitud_vec1 * magnitud_vec2)


def obtener_embedding(texto):
    if not cliente:
        print("Error: No hay cliente de Gemini disponible. Verifica la API key.")
        return None
    try:
        respuesta = cliente.models.embed_content(
            model="gemini-embedding-001",  # Puedes elegir el modelo de embedding que prefieras
            contents=texto
        )
        return respuesta.embeddings[0].values
    except Exception as e:
        print(f"Error al obtener embedding de Gemini: {e}")
        return None

def encontrar_mejores_chunks(pregunta, chunks):
    #Busca cual de los chunks es el más relevante para la pregunta que se haga y devuelve ese chunk para que la IA lo procese
    if not chunks:
        return ""
    
    #Se convierte la pregunta en un vector de embedding para compararla con los chunks
    vector_pregunta = obtener_embedding(pregunta)
    if not vector_pregunta:
        return ""

    mejor_chunk = ""
    max_similitud = -1.0

    for chunk in chunks:
        # Limpiar el chunk y convertirlo en un conjunto de palabras
        vector_chunk = obtener_embedding(chunk)
        if not vector_chunk:
            continue
        similitud = calcular_similitud_coseno(vector_pregunta, vector_chunk) # Incrementar el puntaje por cada coincidencia de palabra entre la pregunta y el chunk

        if similitud > max_similitud:
            max_similitud = similitud
            mejor_chunk = chunk
    
    print(f'Similitud máxima para {pregunta}: {max_similitud}')

    # Umbral de seguridad para evitar devolver chunks irrelevantes 
    if max_similitud < 0.2:
        print("No se encontró un chunk relevante para la pregunta.")
        return ""
    chunk_limpio = " ".join(mejor_chunk.split())  # Eliminar saltos de línea y espacios extra antes de mandarlo a la IA

    return chunk_limpio
