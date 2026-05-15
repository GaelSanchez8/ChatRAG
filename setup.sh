#!/bin/bash
# Script de setup para macOS/Linux

echo "=========================================="
echo "ChatRAG - Setup Automatizado (Linux/macOS)"
echo "=========================================="
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado. Por favor, instálalo primero."
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"
echo ""

# Crear entorno virtual
echo "📦 Creando entorno virtual..."
python3 -m venv venv

# Activar entorno virtual
echo "🔌 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Crear .env desde .env.example si no existe
if [ ! -f .env ]; then
    echo "📝 Creando archivo .env..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANTE: Edita el archivo .env y pega tu GEMINI_API_KEY"
    echo "   Ve a: https://ai.google.dev/ para obtener tu API key"
else
    echo "✅ Archivo .env ya existe"
fi

echo ""
echo "=========================================="
echo "✅ Setup completado!"
echo "=========================================="
echo ""
echo "Próximos pasos:"
echo "1. Edita el archivo .env y pega tu GEMINI_API_KEY"
echo "2. Ejecuta la app: python src/ui/main_ui.py"
echo ""
echo "Para activar el entorno en futuras sesiones, ejecuta:"
echo "   source venv/bin/activate"
echo ""
