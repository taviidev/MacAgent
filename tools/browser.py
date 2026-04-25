def fetch_url(url: str) -> str:
    """Downloads a URL using the verified system python to avoid import issues."""
    import subprocess
    import json
    
    # Script de una sola línea para ejecutar en el python verificado
    py_script = f"""
import requests
from bs4 import BeautifulSoup
import sys

try:
    headers = {{'User-Agent': 'Mozilla/5.0'}}
    r = requests.get('{url}', headers=headers, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')
    for e in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
        e.decompose()
    text = soup.get_text(separator='\\n')
    clean = '\\n'.join([l.strip() for l in text.splitlines() if l.strip()])
    print(clean[:5000])
except Exception as e:
    print(f'Error: {{str(e)}}')
"""
    try:
        # Usamos el path absoluto del python que sabemos que funciona
        python_path = "/Library/Frameworks/Python.framework/Versions/3.14/bin/python3"
        result = subprocess.run(
            [python_path, "-c", py_script],
            capture_output=True,
            text=True,
            timeout=20
        )
        return result.stdout if result.stdout.strip() else f"Error: {result.stderr}"
    except Exception as e:
        return f"Error en el motor de navegación: {str(e)}"
