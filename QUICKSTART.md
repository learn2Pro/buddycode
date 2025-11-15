# Quick Start Guide

Get started with BuddyCode in 5 minutes!

## Installation

The package is already set up in this directory. All dependencies are installed.

## Run Tests

```bash
# Run the test suite
uv run python test_tools.py
```

## Run Examples

```bash
# Run all examples (interactive)
uv run python examples.py

# Or run specific example functions
uv run python -c "from examples import example_1_basic_tool_usage; example_1_basic_tool_usage()"
```

## Quick Usage Examples

### 1. Direct Tool Usage

```python
from buddycode import LsTool, GrepTool, TreeTool, BashTool

# List files
ls = LsTool()
print(ls._run(path=".", long_format=True))

# Search for patterns
grep = GrepTool()
print(grep._run(pattern="import.*langchain", file_pattern="*.py"))

# Show directory tree
tree = TreeTool()
print(tree._run(path=".", max_depth=2))

# Execute bash commands
bash = BashTool()
print(bash._run(command="git status"))

# Edit files
edit = EditTool()
# View file with line numbers
print(edit._run(operation="view", file_path="script.py"))
# Create new file
print(edit._run(operation="create", file_path="new.py", content="# New file\n"))
# Replace text
print(edit._run(operation="str_replace", file_path="config.py", old_str="DEBUG=True", new_str="DEBUG=False"))
```

### 2. With LangChain Agent

```python
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from buddycode import get_file_system_tools

# Set your API key first
# export OPENAI_API_KEY='your-key-here'

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tools = get_file_system_tools()

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Ask questions
response = agent.run("What Python files are in the src directory?")
print(response)
```

### 3. With LangGraph

```python
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from buddycode import get_file_system_tools

llm = ChatOpenAI(model="gpt-4o-mini")
tools = get_file_system_tools()
graph = create_react_agent(llm, tools)

# Use the graph
inputs = {"messages": [("user", "Show me the project structure")]}
for chunk in graph.stream(inputs, stream_mode="values"):
    chunk["messages"][-1].pretty_print()
```

## Tool Reference

### LsTool
- List directory contents
- Options: `show_hidden`, `long_format`, `recursive`

### GrepTool
- Search for text patterns
- Options: `pattern`, `file_pattern`, `case_insensitive`, `context_lines`, `max_results`

### TreeTool
- Display directory tree
- Options: `max_depth`, `show_hidden`, `dirs_only`

### BashTool
- Execute bash commands
- Options: `command`, `working_dir`, `timeout`, `capture_stderr`
- ⚠️ **Security Warning**: Only use in trusted environments

### EditTool
- Text editor for viewing and modifying files
- Operations: `view` (read with line numbers), `create` (new file), `insert` (add at line), `str_replace` (find & replace)
- Options: `operation`, `file_path`, `content`, `line_number`, `start_line`, `end_line`, `old_str`, `new_str`
- 💡 **Best Practice**: Always use `view` before editing

## Next Steps

1. Read the full [README.md](README.md) for comprehensive documentation
2. Explore [examples.py](examples.py) for more use cases
3. Check the [tools.py](src/buddycode/tools.py) source code for implementation details

## Troubleshooting

**Import Error**: Make sure to run with `uv run python` instead of just `python`

**Missing API Key**: Set `OPENAI_API_KEY` environment variable for agent examples

**Permission Errors**: The tools gracefully handle permission errors and continue

## Files in This Project

```
buddycode/
├── src/buddycode/
│   ├── __init__.py          # Package exports
│   └── tools.py             # LsTool, GrepTool, TreeTool implementations
├── README.md                # Full documentation
├── QUICKSTART.md            # This file
├── examples.py              # 9 comprehensive examples
├── test_tools.py            # Test suite
└── pyproject.toml           # Project configuration
```

Happy coding! 🚀
