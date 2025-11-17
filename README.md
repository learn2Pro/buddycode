# BuddyCode

LangChain-based AI coding assistant with file system tools and a beautiful TUI.

**Disclaimer:** 99% code written by Claude.

## Features

- 🎨 **Interactive TUI** - Textual-based terminal interface with markdown rendering
- ⚡ **Token Streaming** - See responses generated character-by-character in real-time
- 🔧 **Tool Visibility** - Watch tool calls, arguments, and results as they happen
- 📋 **Clipboard Copy** - Copy agent responses with Ctrl+C
- 🛠️ **File System Tools** - ls, grep, tree, bash, edit, todo
- 🌐 **LangGraph API** - REST API server with checkpointing and multi-session support
- ✅ **100 Automated Tests** - Comprehensive test coverage with pytest + asyncio
- 🤖 **Natural Language** - Chat with AI agent using plain English

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      BuddyCode System                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐   ┌──────────┐   ┌──────────────────────┐   │
│  │   TUI    │   │ Library  │   │  LangGraph Server    │   │
│  │ (Textual)│   │  (SDK)   │   │   (REST API)         │   │
│  └────┬─────┘   └────┬─────┘   └─────────┬────────────┘   │
│       │              │                   │                 │
│       └──────────────┴───────────────────┘                 │
│                      │                                     │
│              ┌───────▼────────┐                            │
│              │  LangGraph     │                            │
│              │  Agent (ReAct) │                            │
│              └───────┬────────┘                            │
│                      │                                     │
│       ┌──────────────┼──────────────┐                      │
│       │              │              │                      │
│  ┌────▼─────┐  ┌────▼────┐  ┌─────▼──────┐               │
│  │ LLM      │  │ Tools   │  │ Memory     │               │
│  │ (OpenAI) │  │(6 tools)│  │(Checkpoint)│               │
│  └──────────┘  └─────────┘  └────────────┘               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Components:**
- **Interface Layer**: TUI, Python SDK, REST API
- **Agent Layer**: LangGraph orchestration with ReAct pattern
- **Tool Layer**: File system operations (ls, grep, tree, bash, edit, todo)
- **Memory Layer**: InMemorySaver for conversation persistence
- **LLM Layer**: Configurable language model


## Installation

**Requirements:** Python 3.11+

```bash
git clone <repo-url>
cd buddycode
uv pip install -e .  # or: pip install -e .
```

## Quick Start

BuddyCode can be used in three modes:

| Mode | Use Case | Command |
|------|----------|---------|
| **TUI** | Interactive terminal chat | `buddycode` |
| **Library** | Python SDK integration | `from buddycode.react_agent import create_coding_agent` |
| **API** | REST server for apps | `./start_langgraph.sh` |

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

- **Ctrl+Q** - Quit application
- **Ctrl+L** - Clear chat history
- **Ctrl+C** - Copy last agent response to clipboard
- **Enter** - Send message

### Token-Level Streaming

Experience ChatGPT-like real-time responses:

**⚡ Token Streaming** (Green with progress)
- Responses appear character-by-character as generated
- Live character count in status bar
- `🤖 Agent (streaming...)` → `🤖 Agent Response`

**🔧 Tool Calls** (Blue)
- See which tools are invoked instantly
- View tool arguments in formatted JSON

**✅ Tool Results** (Cyan)
- View outputs from tool executions
- Long outputs auto-truncated to 500 chars

Example flow with streaming:
```
User: "Show project structure and find TODOs"

🔧 Tool: tree {"path": ".", "depth": 2}
✅ Result: . ├── src/ └── tests/

🔧 Tool: grep {"pattern": "TODO"}
✅ Result: src/app.py:15: # TODO: implement

🤖 Agent (streaming...)
Found

🤖 Agent (streaming...)
Found 2 directories

🤖 Agent (streaming...)
Found 2 directories and 1 TODO comment. The project is well...

🤖 Agent Response (Final)
Found 2 directories and 1 TODO comment. The project is well-organized
with source code in `src/` and tests in `tests/`.
```

See [STREAMING.md](STREAMING.md) for technical details.

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

### LangGraph Server API

Run the agent as a REST API service using LangGraph:

```bash
# Start LangGraph development server (default port 8123)
./start_langgraph.sh

# Or specify custom port
./start_langgraph.sh 8080

# Or use langgraph CLI directly
uv run langgraph dev --port 8123
```

**Available Endpoints:**

```bash
# Get server info
curl http://localhost:8123/info

# List available assistants
curl http://localhost:8123/assistants

# Create a run
curl -X POST http://localhost:8123/runs/create \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "coding_agent",
    "input": {"messages": [{"role": "user", "content": "Show project structure"}]},
    "config": {"configurable": {"thread_id": "session_1"}}
  }'
```

**Graph Configuration** (`langgraph.json`):

```json
{
  "dependencies": ["."],
  "graphs": {
    "coding_agent": "./src/buddycode/react_agent.py:create_graph"
  },
  "env": ".env"
}
```

**Features:**
- **Checkpointing** - Conversation memory with InMemorySaver
- **Thread Management** - Multiple concurrent sessions via thread_id
- **Streaming** - Real-time token streaming support
- **LangSmith Integration** - Monitor at https://smith.langchain.com

**Python Client Example:**

```python
import requests

response = requests.post(
    "http://localhost:8123/runs/stream",
    json={
        "assistant_id": "coding_agent",
        "input": {"messages": [{"role": "user", "content": "List Python files"}]},
        "config": {"configurable": {"thread_id": "my_session"}},
        "stream_mode": "messages"
    },
    stream=True
)

for line in response.iter_lines():
    if line:
        print(line.decode())
```

**Benefits:**
- **Stateful** - Maintains conversation history per thread
- **Concurrent** - Handle multiple sessions simultaneously
- **Observable** - Integrate with LangSmith for monitoring
- **Deployable** - Production-ready with Docker/Kubernetes

See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment.

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
- `test_tui_streaming.py` - Streaming features (6 tests)

See [tests/README.md](tests/README.md) for details.

### Project Structure

```
buddycode/
├── src/buddycode/
│   ├── tui.py              # Text User Interface
│   ├── react_agent.py      # LangGraph agent with ReAct pattern
│   ├── tools.py            # File system tools
│   └── chat_model.py       # Chat model config
├── tests/                  # 94 automated tests
│   ├── test_tui_*.py       # TUI tests
│   └── conftest.py         # Test fixtures
├── langgraph.json          # LangGraph API configuration
├── start_langgraph.sh      # LangGraph server startup script
├── examples.py             # Usage examples
└── pyproject.toml          # Project config
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# LLM API Configuration
OPENAI_API_KEY="your-api-key-here"

# Or configure your preferred provider
# ANTHROPIC_API_KEY="..."
# COHERE_API_KEY="..."

# LangSmith Tracing (optional)
LANGCHAIN_TRACING_V2="true"
LANGCHAIN_API_KEY="your-langsmith-key"
LANGCHAIN_PROJECT="buddycode"
```

### Agent Configuration

The agent uses LangGraph with:
- **Model**: Configurable via `chat_model.py`
- **Memory**: InMemorySaver for conversation persistence
- **Tools**: 6 file system tools (ls, grep, tree, bash, edit, todo)
- **Prompt**: ReAct pattern with detailed system instructions

## Contributing

1. Fork repository
2. Create feature branch
3. Write tests for changes
4. Ensure all tests pass: `pytest tests/`
5. Submit pull request

## Acknowledgments

- [LangChain](https://www.langchain.com/) - Agent framework and tools
- [LangGraph](https://www.langchain.com/langgraph) - Agent orchestration and API server
- [LangSmith](https://smith.langchain.com/) - Tracing and observability
- [Textual](https://textual.textualize.io/) - Beautiful TUI framework
- Built by [Claude](https://www.anthropic.com/claude) - 99% AI-generated code

