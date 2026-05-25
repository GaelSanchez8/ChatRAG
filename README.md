# 💬 ChatRAG - Chat Inteligente con RAG

**ChatRAG** es una aplicación de escritorio basada en Python que permite interactuar con documentos usando inteligencia artificial. Utiliza **Retrieval Augmented Generation (RAG)** para proporcionar respuestas precisas basadas en el contenido de tus archivos.

## ✨ Características Principales

- 📄 **Carga de Documentos**: Soporta PDF y archivos de texto (.txt)
- 🧠 **RAG (Retrieval Augmented Generation)**: Búsqueda semántica inteligente de contenido
- 💬 **Chat Interactivo**: Interfaz gráfica amigable con historial de conversaciones
- 🔐 **Autenticación Segura**: Registro con verificación de email
- 💾 **Exportación**: Guarda tus conversaciones en JSON o XML
- 🌓 **Tema Oscuro/Claro**: Interfaz adaptable a tu preferencia
- ⚡ **Respuestas Rápidas**: Integración con Google Gemini 2.5 Flash

---

## 👥 Para Usuarios Finales

📖 **¿Cómo instalar y usar ChatRAG?**

Consulta el archivo **[manual_usuario.txt](manual_usuario.txt)** para:

- ✅ Configurar el archivo `.env` paso a paso
- ✅ Obtener tu API key de Google Gemini
- ✅ Crear una base de datos en Supabase (opcional)
- ✅ Ejecutar la aplicación
- ✅ Aprender a usar todas las funciones (cargar archivos, chat, exportar, etc.)

---

## 👨‍💻 Para Desarrolladores

### 🚀 Inicio Rápido

#### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPO>
cd Proyecto
```

#### 2. Ejecutar el setup automático

**Windows:**

```bash
setup.bat
```

**Linux/macOS:**

```bash
bash setup.sh
```

Este script automáticamente:

- Crea el entorno virtual
- Instala todas las dependencias (`requirements.txt`)
- Crea el archivo `.env` desde `.env.example`
- Te pide que añadas tu API key de Gemini

#### 3. Configuración Manual (si prefieres)

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
# o
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Crear .env
cp .env.example .env      # Linux/macOS
# o
copy .env.example .env    # Windows
```

Edita `.env` y añade tu API key de Gemini en:

```
GEMINI_API_KEY=tu_clave_aqui
```

#### 4. Ejecutar la aplicación

```bash
# Desde la raíz del proyecto
python src/ui/main_ui.py
```

### 📋 Requisitos de Desarrollo

- **Python 3.10+**
- **Conexión a Internet**
- **API key de Google Gemini** (gratuita en [ai.google.dev](https://ai.google.dev/)) ⭐ OBLIGATORIO
- **(Opcional)** Supabase PostgreSQL (por defecto usa SQLite local)
- **(Opcional)** Gmail para verificación de email

## 🏗️ Estructura del Proyecto

```
Proyecto/
├── src/
│   ├── logic/              # Lógica de negocio
│   │   ├── auth_manager.py      # Autenticación y encriptación
│   │   ├── document_processor.py # Procesamiento de PDFs
│   │   └── ia_engine.py          # Integración con Gemini
│   └── ui/                       # Interfaz gráfica (PySide6)
│       ├── main_ui.py
│       ├── chat_window.py
│       ├── login_window.py
│       ├── register_window.py
│       └── verify_email_window.py
├── database/               # Gestión de base de datos
│   └── database_manager.py
├── manual_usuario.txt      # 📖 Guía para usuarios finales
├── .env.example            # Plantilla de configuración
├── requirements.txt        # Dependencias Python
├── setup.sh / setup.bat    # Scripts de instalación automática
├── TROUBLESHOOTING.md      # Solución de problemas
└── SECURITY.md             # Pautas de seguridad
```

## 🔐 Seguridad

- ✅ El archivo `.env` está en `.gitignore` (nunca se sube al repositorio)
- ✅ Las contraseñas se hashean con bcrypt (SHA256)
- ✅ Los datos se almacenan en SQLite local o Supabase (tu elección)
- ✅ La API key de Gemini está protegida en `.env`
- ✅ Cada usuario tiene su propia clave API (no se comparten)

## 📚 Documentación Adicional

- **[manual_usuario.txt](manual_usuario.txt)** - Guía completa para usuarios finales
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Solución de problemas comunes
- **[SECURITY.md](SECURITY.md)** - Pautas de seguridad

## 🛠️ Tech Stack

- **Frontend**: PySide6 (Qt para Python)
- **Backend**: Python 3.10+
- **IA**: Google Gemini 2.5 Flash
- **Base de Datos**: SQLite (por defecto) o Supabase PostgreSQL
- **Autenticación**: bcrypt para hashing de contraseñas
- **Email**: Gmail SMTP (opcional)
- **Dependencias**: Ver [requirements.txt](requirements.txt)

## 📝 Licencia

Proyecto final para la materia de Ingeniería de Software - 4to Semestre

## 👥 Equipo de Desarrollo

Equipo de Ingeniería de Software
