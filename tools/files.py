import os

def read_file(path: str) -> str:
    """Reads the content of a file."""
    try:
        # Resolve path to be absolute if it's relative
        if not os.path.isabs(path):
            # For now, let's assume relative to root or home if not specified
            # But better to require absolute paths for MCP tools
            pass
            
        if not os.path.exists(path):
            return f"Error: File not found at {path}"
            
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def list_dir(path: str) -> str:
    """Lists the contents of a directory."""
    try:
        if not os.path.exists(path):
            return f"Error: Directory not found at {path}"
            
        if not os.path.isdir(path):
            return f"Error: {path} is not a directory"
            
        items = os.listdir(path)
        # Sort items (directories first, then files)
        items.sort(key=lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower()))
        
        result = []
        for item in items:
            full_path = os.path.join(path, item)
            is_dir = "[DIR]" if os.path.isdir(full_path) else "[FILE]"
            result.append(f"{is_dir} {item}")
            
        return "\n".join(result) if result else "(Empty directory)"
    except Exception as e:
        return f"Error listing directory: {str(e)}"

def write_file(path: str, content: str) -> str:
    """Writes content to a file."""
    try:
        # Ensure parent directory exists
        parent = os.path.dirname(path)
        if parent and not os.path.exists(parent):
            os.makedirs(parent)
            
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Success: File written to {path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

def grep_search(pattern: str, path: str) -> str:
    """Performs a grep search in a directory, excluding common noise."""
    import subprocess
    try:
        # -r: recursive, -n: line number, -i: case insensitive, -I: ignore binary files
        # --exclude-dir: exclude node_modules, .git, etc.
        command = [
            'grep', '-rnI', 
            '--exclude-dir=node_modules', 
            '--exclude-dir=.git', 
            '--exclude-dir=dist', 
            '--exclude-dir=.next',
            pattern, path
        ]
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30
        )
        output = result.stdout + result.stderr
        return output if output.strip() else f"No matches found for '{pattern}' in {path}"
    except Exception as e:
        return f"Error performing grep: {str(e)}"
