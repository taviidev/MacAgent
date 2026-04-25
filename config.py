import os

# --- CONFIGURACIÓN DE IDENTIDAD ---
USER_NAME = "jorgetamaral"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- CONFIGURACIÓN DE IA (EL CEREBRO) ---
# Opciones disponibles: "local" (Llama.cpp), "ollama", "openai", "anthropic"
AI_PROVIDER = "local" 

# Modelo a utilizar
# Local/Ollama: Nombre del modelo cargado
# OpenAI: "gpt-4o", "gpt-3.5-turbo", etc.
# Anthropic: "claude-3-5-sonnet-20240620"
AI_MODEL = "deepseek-r1"

# URL del servidor para proveedores locales
# Llama.cpp por defecto: http://127.0.0.1:8000
# Ollama por defecto: http://127.0.0.1:11434
AI_API_URL = "http://127.0.0.1:8000"

# API Key para proveedores de nube (ignorar si es local)
AI_API_KEY = "sk-your-key-here"

# --- RUTAS DE SISTEMA ---
DEBUG_LOG_PATH = os.path.join(BASE_DIR, "debug_llm.txt")
HISTORY_FILE_PATH = os.path.join(BASE_DIR, "chat_history.json")
