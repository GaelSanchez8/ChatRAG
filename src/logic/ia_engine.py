import os 
from google import genai
from dotenv import load_dotenv
import concurrent.futures #Para manejar llamadas asíncronas a la API de Gemini y evitar bloqueos en la interfaz de usuario
load_dotenv()

#Obetener la clave de la API de Gemini desde las variables de entorno
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY: 
    cliente = genai.Client(api_key=API_KEY)
else:
    cliente = None

def _llamar_gemini_interno(pregunta, contexto=""):
    #Toma el mejor chunk y se lo pasa a gemini
    if not cliente:
        return "Error: No se encontró la API key, en el .env."
    if not contexto:
        return "[No se encontraron fragmentos relevantes en el documento para esta pregunta específica]."
    
    #El prompt RAG (obliga a la IA a no inventar respuestas y a usar solo el contexto proporcionado
    prompt = f"""
    Eres un asistente experto de análisis de documentos. 
    Responde a la pregunta del usuario basándote ÚNICAMENTE en la información proporcionada en el siguiente contexto. 
    Si la respuesta no se encuentra en el contexto, indica claramente que no tienes suficiente información en el documento.
    
    Contexto del documento:
    {contexto}
    
    Pregunta del usuario:
    {pregunta}
    """ 

    try:
        #LLamada a la API de Gemini para obtener la respuesta
        respuesta = cliente.models.generate_content(
            model="gemini-2.5-flash",  # Puedes elegir el modelo que prefieras
            contents=prompt
        )
        return respuesta.text.strip()
    except Exception as e:
        return f"Error de conexión con la API de Gemini: {str(e)}"
    

def procesar_pregunta_ia(pregunta, contexto):
    "Le pone a la IA un cronometro estricto para dar un error de timeout si la respuesta tarda demasiado, evitando bloqueos en la interfaz"""
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(_llamar_gemini_interno, pregunta, contexto)

        try:
            respuesta = future.result(timeout=30)
            return respuesta
        except concurrent.futures.TimeoutError:
            return "Error: La respuesta de la IA tardó demasiado tiempo. Por favor, intenta de nuevo."
        except Exception as e:
            #Se captura cualquier otro error que pueda ocurrir durante la llamada a la API
            return f"Error de conexión con la API de Gemini: {str(e)}"