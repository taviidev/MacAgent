import asyncio
import sys
import os
import json
import re
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from config import BASE_DIR, AI_API_URL

# Librerías de UI
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.markdown import Markdown
from rich.status import Status
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory

# Importar el stream de llm (usamos importación directa para mayor facilidad)
from tools.llm import stream_llama

console = Console()

async def run_agent():
    # Configuración del servidor MCP
    server_params = StdioServerParameters(
        command="/Library/Frameworks/Python.framework/Versions/3.14/bin/python3",
        args=[os.path.join(BASE_DIR, "server.py")],
        env=os.environ.copy()
    )

    console.print(Panel.fit("[bold blue]🤖 MacAgent CLI Premium v2.0[/bold blue]\n[italic]Tu copiloto local e inteligente[/italic]", border_style="blue"))
    
    # Sesión de prompt con historial
    prompt_session = PromptSession(history=FileHistory(os.path.join(BASE_DIR, ".prompt_history")))

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            while True:
                try:
                    user_input = await prompt_session.prompt_async("\n👤 [User]: ")
                except (EOFError, KeyboardInterrupt):
                    break

                if user_input.lower() in ["salir", "exit", "quit"]:
                    break

                current_prompt = user_input
                last_command = None
                
                while True:
                    # 1. STREAMING de la respuesta
                    agent_full_text = ""
                    console.print("\n[bold blue]🤖 MacAgent:[/bold blue]")
                    
                    with Live("", console=console, refresh_per_second=10) as live:
                        for chunk in stream_llama(current_prompt):
                            agent_full_text += chunk
                            # Limpieza de pensamientos y roles
                            display_text = re.sub(r"<think>.*?</think>", "💭 *Pensando...*\n", agent_full_text, flags=re.DOTALL)
                            display_text = re.sub(r"^\s*(Assistant|User|System):\s*", "", display_text, flags=re.IGNORECASE | re.MULTILINE)
                            live.update(Markdown(display_text))

                    # 2. Buscar si hay comandos EJECUTAR o EJECUTOR (insensible a mayúsculas)
                    match = re.search(r"EJECUT[AO]R:\s*(\w+)\s*(.*)", agent_full_text, re.IGNORECASE)
                    if not match:
                        break

                    tool_name = match.group(1).strip()
                    tool_args_raw = match.group(2).strip().strip("'").strip('"')
                    current_command = f"{tool_name}:{tool_args_raw}"

                    if current_command == last_command:
                        console.print("[bold red]⚠️ Detectado bucle infinito. Forzando al agente a concluir.[/bold red]")
                        current_prompt = "Ya has ejecutado ese comando con el mismo resultado. Por favor, termina la tarea con la información que tienes."
                        last_command = None # Reset para permitir el siguiente paso
                        continue

                    last_command = current_command

                    # 3. Ejecución con SPINNER
                    with Status(f"[bold yellow]⚙️  Ejecutando {tool_name}...[/bold yellow]", console=console) as status:
                        args = {}
                        if tool_name == "shell": args = {"command": tool_args_raw}
                        elif tool_name in ["read_file", "list_dir"]: args = {"path": tool_args_raw}
                        elif tool_name == "fetch_url": args = {"url": tool_args_raw}
                        elif tool_name == "write_file":
                            parts = tool_args_raw.split(" ", 1)
                            args = {"path": parts[0], "content": parts[1] if len(parts) > 1 else ""}

                        try:
                            tool_result = await session.call_tool(tool_name, arguments=args)
                            result_text = tool_result.content[0].text
                            console.print(f"[green]✅ {tool_name} completado.[/green]")
                            
                            # Pasar el resultado al siguiente turno
                            current_prompt = f"RESULTADO DE {tool_name}:\n{result_text}\n\nContinúa según este resultado."
                        except Exception as e:
                            console.print(f"[red]❌ Error: {e}[/red]")
                            break

if __name__ == "__main__":
    try:
        asyncio.run(run_agent())
    except KeyboardInterrupt:
        console.print("\n[bold red]👋 ¡Hasta pronto![/bold red]")
