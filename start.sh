#!/bin/bash

# Script de inicio para el Bot de Twitter - Tweets Cristianos
# Versión para sistemas Unix/Linux/macOS

echo "🐦 Iniciando Bot de Twitter - Tweets Cristianos"
echo "=" * 50

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "❌ Error: Python no está instalado"
        echo "Por favor instala Python 3.7 o superior"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "✅ Python encontrado: $($PYTHON_CMD --version)"

# Verificar si existe el archivo .env
if [ ! -f ".env" ]; then
    echo "⚠️  Archivo .env no encontrado"
    echo "Creando archivo .env de ejemplo..."
    cat > .env << EOF
# Credenciales de Twitter API
API_KEY=tu_api_key_aqui
API_SECRET=tu_api_secret_aqui
ACCESS_TOKEN=tu_access_token_aqui
ACCESS_SECRET=tu_access_secret_aqui
BEARER_TOKEN=tu_bearer_token_aqui
EOF
    echo "📝 Archivo .env creado. Por favor completa las credenciales y ejecuta el script nuevamente."
    exit 1
fi

echo "✅ Archivo .env encontrado"

# Verificar si existe requirements.txt
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt no encontrado"
    exit 1
fi

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    $PYTHON_CMD -m venv venv
fi

# Activar entorno virtual
echo "🔄 Activando entorno virtual..."
source venv/bin/activate

# Actualizar pip
echo "⬆️  Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install -r requirements.txt

# Ejecutar el bot
echo "🚀 Iniciando el bot..."
echo ""
$PYTHON_CMD publicar_tuits.py

# Desactivar entorno virtual al finalizar
deactivate

echo ""
echo "✅ Bot finalizado. ¡Que Dios te bendiga!"
