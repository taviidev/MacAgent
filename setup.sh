#!/bin/bash

# --- MacAgent Setup Script ---
echo "🤖 Iniciando instalación de MacAgent..."

# 1. Verificar Python 3
if ! command -v python3 &> /dev/null
then
    echo "❌ Error: Python 3 no está instalado. Por favor, instálalo antes de seguir."
    exit
fi

# 2. Instalar dependencias
echo "📦 Instalando dependencias de Python (mcp, requests, beautifulsoup4, rich, prompt_toolkit)..."
python3 -m pip install mcp requests beautifulsoup4 rich prompt_toolkit

# 3. Crear archivos necesarios si no existen
if [ ! -f "chat_history.json" ]; then
    echo "[]" > chat_history.json
    echo "📝 Historial de chat inicializado."
fi

if [ ! -f "debug_llm.txt" ]; then
    touch debug_llm.txt
    echo "📝 Archivo de debug creado."
fi

# 4. Finalizar
echo ""
echo "✅ ¡Instalación completada con éxito!"
echo "------------------------------------------------"
echo "🚀 Para usarlo con Claude Desktop, sigue las instrucciones del README.md"
echo "💻 Para usar la terminal, ejecuta: python3 client.py"
echo "------------------------------------------------"
