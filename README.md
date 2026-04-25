# 🤖 MacAgent

**MacAgent** is an autonomous AI system orchestrator for macOS. Built on the **Model Context Protocol (MCP)**, it connects your favorite AI brain with your system's power.

---

## ❓ Why MacAgent?

While tools like **Aider** focus strictly on code editing within a repository, **MacAgent** is a general-purpose system assistant.

- **Privacy & Cost**: Use local models (Ollama/Llama.cpp) to save money and keep data private.
- **System Orchestration**: It doesn't just edit code; it manages your terminal, installs dependencies, and navigates the web.
- **Token Efficiency (Hybrid Workflow)**: The perfect companion for cloud agents like **Antigravity**. Use cloud models for high-level architecture and planning, but delegate "expensive" or repetitive tasks (writing boilerplate, tests, or running shell commands) to MacAgent. **Save up to 90% in token costs.**
- **MCP Native**: Unlike closed tools, MacAgent uses the industry-standard Model Context Protocol. This means it works inside **Antigravity**, **Claude Desktop**, **Claude Code**, and **Cursor** simultaneously.
- **Smart Loop**: It doesn't just give you code; it executes it, checks for errors, and fixes them automatically until the job is done.

---

## 🚀 Installation

1.  **Clone this repo** to your local machine.
2.  **Run the automated setup**:
    ```bash
    bash setup.sh
    ```
    This will install the necessary dependencies (`rich`, `prompt_toolkit`, etc.).

---

## 💻 Usage Modes

### 1. Antigravity & Cursor
Since MacAgent is a standard MCP server, you can add it to Antigravity or Cursor by pointing to the `server.py` file using your Python path. This allows the cloud agent to delegate local tasks to your Mac.

### 2. The Premium CLI
For a fast, interactive terminal experience with streaming and markdown:
```bash
python3 client.py
```

### 3. Claude Code (Official CLI)
To add MacAgent as a persistent tool in Claude Code:
```bash
claude mcp add --transport stdio --scope user mac-code-agent -- python3 /PATH/TO/YOUR/FOLDER/server.py
```

### 4. Claude Desktop
Add this to your `claude_desktop_config.json`:
```json
"mcpServers": {
  "mac-code-agent": {
    "command": "python3",
    "args": ["/PATH/TO/YOUR/FOLDER/server.py"]
  }
}
```

---

## 🔥 Features

- **Shell Access**: Complete control of your Mac terminal (Git, NPM, Brew).
- **Web Browsing**: Built-in tool to fetch and read real-time web documentation.
- **Universal Memory**: Persistent and optimized chat history for local models.
- **Multi-Model Support**: Switch between Llama.cpp, Ollama, or OpenAI via `config.py`.

---

## 🛡️ Safety
MacAgent has system access. Use it in trusted directories. It is designed to be your local "intern" that never gets tired.

---

*Created by TaviDev*
