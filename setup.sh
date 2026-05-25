#!/bin/bash
# Script de setup para macOS/Linux

echo "=========================================="
echo "ChatRAG - Setup Automatizado (Linux/macOS)"
echo "=========================================="
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo " Python 3 no está instalado. Por favor, instálalo primero."
    exit 1
fi

echo " Python encontrado: $(python3 --version)"
echo ""

# Crear entorno virtual
echo " Creando entorno virtual..."
python3 -m venv venv

# Activar entorno virtual
echo " Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo " Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Crear .env desde .env.example si no existe
if [ ! -f .env ]; then
    echo " Creando archivo .env..."
    cp .env.example .env
else
    echo " Archivo .env ya existe"
fi

echo ""
echo "=========================================="
echo " Setup completado!"
echo "=========================================="
echo ""
echo " PRÓXIMOS PASOS - OBLIGATORIO:"
echo ""
echo "1. Obtén tu API key de Google Gemini (GRATIS):"
echo "   → Ve a: https://ai.google.dev/"
echo "   → Haz clic en 'Get API Key'"
echo "   → Copia tu API key"
echo ""
echo "2. Edita el archivo .env y pega tu GEMINI_API_KEY"
echo ""
echo "3. Ejecuta la app:"
echo "   python src/ui/main_ui.py"
echo ""
echo " Para instrucciones completas (incluyendo opcionales Supabase/Email):"
echo "   Lee: manual_usuario.txt"
echo ""
echo "Para futuras sesiones, activa el entorno con:"
echo "   source venv/bin/activate"
echo ""
