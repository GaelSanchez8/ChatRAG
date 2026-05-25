# 🆘 Solución de Problemas - ChatRAG

## ❌ Error: ModuleNotFoundError: No module named 'database'

**Causa**: Estás ejecutando el script desde dentro de la carpeta `src/`

**Solución**:

```bash
# ❌ INCORRECTO
cd src
python ui/main_ui.py

# ✅ CORRECTO
cd ..  # Vuelve a la raíz del proyecto
python src/ui/main_ui.py
```

**Explicación**: El proyecto debe ejecutarse **siempre desde la carpeta raíz** (donde está `requirements.txt`), no desde dentro de `src/`.

---

## ❌ Error: ModuleNotFoundError: No module named 'PySide6'

**Causa**: Las dependencias no están instaladas

**Solución**:

```bash
# Asegúrate de estar en la raíz del proyecto
pip install -r requirements.txt
```

---

## ❌ Error: "No se encontró la API key, en el .env"

**Causa**: El archivo `.env` no existe o `GEMINI_API_KEY` está vacío ( ES OBLIGATORIO)

**Solución**:

1. Copia el archivo de ejemplo:

   ```bash
   cp .env.example .env     # Linux/macOS
   copy .env.example .env   # Windows
   ```

2. Abre el archivo `.env` en tu editor y reemplaza:

   ```
   GEMINI_API_KEY=tu_api_key_de_gemini_aqui
   ```

   con tu API key real de Google Gemini

3. Obtén una API key en: https://ai.google.dev/
   - Haz clic en "Get API Key"
   - Crea una nueva o usa una existente
   - Copia la clave (sin espacios)

4. Reinicia la aplicación

---

## ❌ Error: "Error de conexión con la API de Gemini"

**Causa**: Tu API key es inválida, ha expirado, o no tienes conexión a Internet

**Soluciones**:

1. Verifica que tu **API key es correcta** (copia-pégala desde Google AI Studio)
2. Verifica que tu **conexión a Internet** está activa
3. Verifica que **no hayas excedido** los límites gratuitos de Google AI
4. Si es una API key nueva, espera unos minutos antes de usar (a veces tarda en activarse)

---

## ⚠️ La aplicación se abre pero la interfaz se ve congelada

**Causa**: La API de Gemini está procesando una respuesta

**Solución**:
Espera a que termine. Verás "Procesando..." en el chat mientras se espera la respuesta.


## ❌ Error: No se envía email de verificación (pero la app funciona)

**Causa**: `EMAIL_USER` y `EMAIL_PASSWORD` están vacíos (es OPCIONAL)

**Solución - Para usar email real:**

1. Abre tu `.env` y completa:
   ```
   EMAIL_USER=tu_email@gmail.com
   EMAIL_PASSWORD=xxxx xxxx xxxx xxxx
   ```

2. Para generar contraseña de aplicación:
   - Ve a https://myaccount.google.com/apppasswords
   - Selecciona "Mail" y tu dispositivo
   - Se generará una contraseña de 16 caracteres
   - Cópiala **sin espacios** en `EMAIL_PASSWORD`

3. Reinicia la app

**Alternativa - Usar consola (default):**
Si dejas `EMAIL_USER` y `EMAIL_PASSWORD` en blanco, los códigos se imprimirán en la consola y la app funcionará igual.

---

## ❌ Error: "psycopg2" o problemas de conexión a Supabase

**Causa**: Supabase está mal configurado o no está disponible

**Solución:**

1. **Opción A - Volver a SQLite (más simple):**
   - Abre `.env` y deja en blanco:
     ```
     SUPABASE_HOST=
     SUPABASE_DB_PORT=
     SUPABASE_DB_NAME=
     SUPABASE_DB_USER=
     SUPABASE_DB_PASSWORD=
     ```
   - Reinicia: la app usará SQLite automáticamente

2. **Opción B - Verificar credenciales de Supabase:**
   - Verifica que todos los datos en `SUPABASE_*` sean correctos
   - Comprueba tu conexión a Internet
   - Intenta conectar desde la consola:
     ```bash
     psql -h tu_host.supabase.co -U postgres -d postgres
     ```

---

## 📋 Estructura esperada del proyecto

Si clonaste el repo y aún tienes problemas, verifica que la estructura sea:

```
Proyecto/
├── .env                 ← Créalo copiando .env.example
├── .env.example         ← Plantilla de .env
├── .gitignore
├── README.md
├── SETUP.md
├── TROUBLESHOOTING.md   ← Este archivo
├── requirements.txt
├── setup.sh             ← Para Linux/macOS
├── setup.bat            ← Para Windows
├── data/
│   └── chatbot_rag.db
├── database/
│   ├── __init__.py
│   ├── database_manager.py
│   └── creacion_db.py
├── src/
│   ├── __init__.py
│   ├── logic/
│   │   ├── __init__.py
│   │   ├── auth_manager.py
│   │   ├── document_processor.py
│   │   └── ia_engine.py
│   └── ui/
│       └── main_ui.py
└── docs/
```

---

## 🚀 Usando los scripts de setup automático

**Para Windows**:

```bash
setup.bat
```

**Para Linux/macOS**:

```bash
chmod +x setup.sh
./setup.sh
```

Estos scripts hacen automáticamente:

- Crear el entorno virtual
- Instalar todas las dependencias
- Crear el archivo `.env` (de `.env.example`)

---

##  Configuración Simplificada

**La app funcionará con solo esto:**
```
GEMINI_API_KEY=tu_clave_aqui
```

**Todo lo demás es opcional:**
- Sin Supabase → Usa SQLite local
- Sin Email → Los códigos se imprimen en consola
- Sin internet → Fallaría la API de Gemini, pero el login/registro funcionaría

---

