# BuddyCode

LangChain-based AI coding assistant with file system tools and a beautiful TUI.

**Disclaimer:** 99% code written by Claude.

## Features

- 🎨 **Interactive TUI** - Textual-based terminal interface with markdown rendering
- 🛠️ **File System Tools** - ls, grep, tree, bash, edit, todo
- ✅ **58 Automated Tests** - Comprehensive test coverage with pytest + asyncio
- 🤖 **Natural Language** - Chat with AI agent using plain English

## Installation

**Requirements:** Python 3.11+

```bash
git clone <repo-url>
cd buddycode
uv pip install -e .  # or: pip install -e .
```

## Quick Start

### Launch TUI

```bash
buddycode  # Simplest method

# Alternatives:
uv run python -m buddycode.tui
python -m buddycode.tui
```

### Usage Examples

**Explore codebase:**
```
"Show me the project structure"
"List all Python files in src/"
"Find all TODO comments"
```

**Edit files:**
```
"Show contents of README.md"
"Create a Button component in components/Button.jsx"
"Fix the import error on line 15"
```

**Run commands:**
```
"Run pytest tests/"
"Check git status"
"Install dependencies"
```

**Manage tasks:**
```
"Create a todo list for the login feature"
```

### Available Tools

| Tool | Description | Example |
|------|-------------|---------|
| **ls** | List files/directories | "List Python files" |
| **grep** | Search in files | "Find 'import React'" |
| **tree** | Directory structure | "Show project tree" |
| **edit** | View/create/modify files | "Edit app.py" |
| **bash** | Execute commands | "Run tests" |
| **todo** | Task management | "Show my tasks" |

### Keyboard Shortcuts

- **Ctrl+C** - Quit
- **Ctrl+L** - Clear chat
- **Enter** - Send message

### Use as Library

```python
from buddycode.react_agent import create_coding_agent

agent = create_coding_agent()
config = {"configurable": {"thread_id": "my_session"}}
result = agent.invoke(
    {"messages": [("user", "Show me the project structure")]},
    config
)
```

## Development

### Run Tests

```bash
# Install dev dependencies
uv pip install -e ".[dev]"

# Run all 58 tests
pytest tests/

# With coverage
pytest tests/ --cov=buddycode.tui --cov-report=html
```

**Test files:**
- `test_tui_comprehensive.py` - Core functionality (24 tests)
- `test_tui_edge_cases.py` - Edge cases & stress tests (18 tests)
- `test_tui_widgets.py` - Widget tests (16 tests)

See [tests/README.md](tests/README.md) for details.

### Project Structure

```
buddycode/
├── src/buddycode/
│   ├── tui.py           # Text User Interface
│   ├── react_agent.py   # LangChain agent
│   ├── tools.py         # File system tools
│   └── chat_model.py    # Chat model config
├── tests/               # 58 automated tests
├── examples.py          # Usage examples
└── pyproject.toml       # Project config
```

## Configuration

```bash
export OPENAI_API_KEY="your-api-key"
# Or configure your preferred LLM provider
```

## Contributing

1. Fork repository
2. Create feature branch
3. Write tests for changes
4. Ensure all tests pass: `pytest tests/`
5. Submit pull request

## Acknowledgments

- [LangChain](https://www.langchain.com/) & [LangGraph](https://www.langchain.com/langgraph)
- [Textual](https://textual.textualize.io/) TUI framework
- Built by [Claude](https://www.anthropic.com/claude)
