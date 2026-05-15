# 📚 ChatRAG - Guía de Configuración para el Equipo

## 🚀 Instrucciones de Instalación

### 1. **Clonar el Repositorio**

```bash
git clone <URL_DEL_REPO>
cd Proyecto
```

### 2. **Crear un Entorno Virtual**

```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. **Instalar Dependencias**

```bash
pip install -r requirements.txt
```

### 4. **Configurar la API de Google Gemini**

#### a. Obtener la API Key

1. Ve a [Google AI Studio](https://ai.google.dev/)
2. Haz clic en "Get API Key"
3. Crea una nueva API key (o usa una existente)
4. Copia la key

#### b. Crear el archivo `.env`

```bash
# Copia el archivo .env.example
cp .env.example .env

# O en Windows:
copy .env.example .env
```

#### c. Editar `.env` y pegar tu API Key

```
GEMINI_API_KEY=tu_api_key_aqui
```

⚠️ **IMPORTANTE**: Nunca hagas commit del archivo `.env` - ya está en `.gitignore`

### 5. **Ejecutar la Aplicación**

⚠️ **IMPORTANTE**: Siempre ejecuta desde la **raíz del proyecto** (donde está `requirements.txt` y la carpeta `src/`)

```bash
# ✓ CORRECTO - Estando en la carpeta raíz del proyecto (Proyecto/)
python src/ui/main_ui.py

# ✗ INCORRECTO - NO hagas cd src primero
# cd src
# python ui/main_ui.py
```

**Paso a paso:**

1. Abre la terminal/cmd en la carpeta raíz del proyecto
2. Asegúrate de haber activado el entorno virtual
3. Ejecuta: `python src/ui/main_ui.py`
4. La aplicación se abrirá en una ventana nueva

## 📋 Estructura del Proyecto

```
Proyecto/
├── src/
│   ├── logic/
│   │   ├── auth_manager.py      # Autenticación y encriptación
│   │   ├── document_processor.py # Procesamiento de PDFs y chunks
│   │   └── ia_engine.py          # Motor de IA (Gemini)
│   └── ui/
│       └── main_ui.py            # Interfaz gráfica (PySide6)
├── database/
│   ├── database_manager.py       # Gestión de SQLite
│   └── creacion_db.py            # Creación de esquema
├── data/
│   └── chatbot_rag.db            # Base de datos SQLite
└── requirements.txt              # Dependencias
```

## 🔍 Funcionalidades Principales

- 📄 **Carga de Documentos**: Soporta PDF y archivos TXT
- 🧠 **RAG (Retrieval Augmented Generation)**: Búsqueda semántica de chunks
- 💬 **Chat Interactivo**: Interfaz gráfica para hacer preguntas
- 🔐 **Seguridad**: Contraseñas encriptadas con bcrypt
- 💾 **Base de Datos**: Almacenamiento de conversaciones

## 🤖 Cómo Funciona el Chatbot

1. **Carga de Documento**: El usuario carga un PDF o TXT
2. **Extracción de Texto**: Se extrae el texto del documento
3. **Chunking**: El texto se divide en fragmentos (chunks) de ~1000 caracteres
4. **Búsqueda Semántica**: Cuando haces una pregunta, se busca el chunk más relevante usando embeddings de Google Gemini
5. **Generación de Respuesta**: El modelo Gemini 2.5 Flash responde basándose SOLO en el contexto del chunk (RAG)

## ⚙️ Variables de Entorno

| Variable         | Descripción                                                      |
| ---------------- | ---------------------------------------------------------------- |
| `GEMINI_API_KEY` | Clave API de Google Gemini (obtén una en https://ai.google.dev/) |

## 📱 Requisitos del Sistema

- Python 3.8+
- 4GB RAM mínimo
- Conexión a Internet (para usar Google Gemini API)

## 🆘 Solución de Problemas

### "Error: No se encontró la API key, en el .env"

- Verifica que el archivo `.env` existe en la raíz del proyecto
- Asegúrate de que `GEMINI_API_KEY` está correctamente configurada
- Reinicia la aplicación después de crear/editar `.env`

### "Error de conexión con la API de Gemini"

- Verifica tu conexión a Internet
- Comprueba que tu API key es válida
- Asegúrate de no haber excedido los límites gratuitos de Google AI

### "ImportError: No module named 'PySide6'"

- Ejecuta: `pip install -r requirements.txt`
- Asegúrate de estar en el entorno virtual activado

## 📝 Notas Importantes

- ⚠️ **NUNCA** compartas el `.env` o publiques tu API key en el repositorio
- Las conversaciones se almacenan en `data/chatbot_rag.db`
- El modelo actual usa `gemini-2.5-flash` - puedes cambiar el modelo en `src/logic/ia_engine.py`

## 👥 Para Colaboradores

1. Clona el repo
2. Crea tu propio `.env` con tu API key
3. No hagas commit del `.env`
4. Si cambias modelos o dependencias, actualiza `requirements.txt`

---

¿Problemas? Crea un issue en el repositorio o contacta al equipo.
