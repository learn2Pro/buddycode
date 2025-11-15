# BuddyCode

LangChain-based AI coding assistant with file system tools and a beautiful TUI.

**Disclaimer:** 99% code written by Claude.

## Features

### 🎨 Beautiful TUI (Text User Interface)
- Interactive terminal interface powered by [Textual](https://textual.textualize.io/)
- Real-time chat with the coding agent
- Markdown rendering for agent responses
- Status tracking and progress indicators

### 🛠️ Powerful File System Tools
LangChain-compatible tools for AI agents:
- **ls** - List directory contents
- **grep** - Search patterns in files
- **tree** - Display directory structure
- **bash** - Execute shell commands
- **edit** - View/create/modify files
- **todo** - Manage task lists

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd buddycode

# Install with uv (recommended)
uv pip install -e .

# Or with pip
pip install -e .
```

**Requirements:** Python 3.11+, langchain, langgraph, textual

## Quick Start

### 🚀 Launch the TUI
```bash
# Method 1: Using the installed command
buddycode

# Method 2: Using Python module
uv run python -m buddycode.tui

# Method 3: Run the test script
uv run python test_tui.py
```

### 📚 Use as a Library
```python
from buddycode.react_agent import create_coding_agent

# Create the agent
agent = create_coding_agent()

# Chat with the agent
config = {"configurable": {"thread_id": "my_session"}}
result = agent.invoke(
    {"messages": [("user", "Show me the project structure")]},
    config
)

# Use individual tools
from buddycode.tools import get_file_system_tools
tools = get_file_system_tools()  # ls, grep, tree, bash, edit, todo
```