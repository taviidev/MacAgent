import requests
import json
import os
from config import AI_PROVIDER, AI_MODEL, AI_API_URL, AI_API_KEY, HISTORY_FILE_PATH

# Configuración del historial (10 intercambios = 20 mensajes + System Prompt)
MAX_HISTORY = 10

import getpass

SYSTEM_PROMPT = f"""ESTÁS EN MODO AGENTE AUTÓNOMO. Eres 'MacAgent', un asistente de ingeniería de software para macOS de {getpass.getuser()}.

REGLA DE ORO (PROHIBICIÓN): Está TERMINANTEMENTE PROHIBIDO usar 'EJECUTAR' para saludos, bromas o charla trivial. Responde con texto normal. Solo usa herramientas para tareas técnicas.

HERRAMIENTAS:
1. shell: Comandos de sistema.
2. read_file / write_file: Manejo de archivos.
3. list_dir / grep_search: Navegación y búsqueda.
4. fetch_url: Documentación web.

FORMATO DE ACCIÓN:
EJECUTAR: [herramienta] [parámetros]
(Tu respuesta debe terminar inmediatamente después del comando).

Actúa de forma profesional y eficiente."""

def load_history():
    if os.path.exists(HISTORY_FILE_PATH):
        try:
            with open(HISTORY_FILE_PATH, 'r') as f:
                history = json.load(f)
                if not history or history[0].get("role") != "system":
                    history.insert(0, {"role": "system", "content": SYSTEM_PROMPT})
                else:
                    history[0]["content"] = SYSTEM_PROMPT
                return history
        except:
            return [{"role": "system", "content": SYSTEM_PROMPT}]
    return [{"role": "system", "content": SYSTEM_PROMPT}]

def save_history(history):
    if len(history) > (MAX_HISTORY * 2) + 1:
        system_msg = history[0]
        recent_msgs = history[-(MAX_HISTORY * 2):]
        history = [system_msg] + recent_msgs
    
    with open(HISTORY_FILE_PATH, 'w') as f:
        json.dump(history, f, indent=2)

def stream_llama(prompt: str):
    """Generador universal que soporta múltiples proveedores."""
    history = load_history()
    history.append({"role": "user", "content": prompt})
    
    full_response = ""
    
    # --- PROVEEDOR: LOCAL (LLAMA.CPP) ---
    if AI_PROVIDER == "local":
        url = f"{AI_API_URL}/completion"
        formatted_prompt = ""
        for msg in history:
            role = "System" if msg["role"] == "system" else ("User" if msg["role"] == "user" else "Assistant")
            formatted_prompt += f"{role}: {msg['content']}\n"
        formatted_prompt += "Assistant: "

        payload = {
            "prompt": formatted_prompt,
            "stream": True,
            "n_predict": 1024,
            "stop": ["User:", "\nUser:", "System:", "\nSystem:"]
        }
        
        try:
            response = requests.post(url, json=payload, stream=True, timeout=60)
            for line in response.iter_lines():
                if line:
                    decoded = line.decode('utf-8')
                    if decoded.startswith("data: "):
                        data = json.loads(decoded[6:])
                        chunk = data.get("content", "")
                        full_response += chunk
                        yield chunk
        except Exception as e:
            yield f"Error Local: {e}"

    # --- PROVEEDOR: OLLAMA ---
    elif AI_PROVIDER == "ollama":
        url = f"{AI_API_URL}/api/chat"
        payload = {
            "model": AI_MODEL,
            "messages": history,
            "stream": True
        }
        try:
            response = requests.post(url, json=payload, stream=True, timeout=60)
            for line in response.iter_lines():
                if line:
                    data = json.loads(line.decode('utf-8'))
                    chunk = data.get("message", {}).get("content", "")
                    full_response += chunk
                    yield chunk
        except Exception as e:
            yield f"Error Ollama: {e}"

    # --- PROVEEDOR: OPENAI ---
    elif AI_PROVIDER == "openai":
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {AI_API_KEY}"}
        payload = {
            "model": AI_MODEL,
            "messages": history,
            "stream": True
        }
        try:
            response = requests.post(url, headers=headers, json=payload, stream=True, timeout=60)
            for line in response.iter_lines():
                if line:
                    decoded = line.decode('utf-8')
                    if decoded.startswith("data: ") and decoded != "data: [DONE]":
                        data = json.loads(decoded[6:])
                        chunk = data['choices'][0]['delta'].get('content', '')
                        full_response += chunk
                        yield chunk
        except Exception as e:
            yield f"Error OpenAI: {e}"

    # Guardar resultado final
    history.append({"role": "assistant", "content": full_response})
    save_history(history)

def call_llama(prompt: str) -> str:
    full_text = ""
    for chunk in stream_llama(prompt):
        full_text += chunk
    return full_text
