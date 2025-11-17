"""
BuddyCode - LangChain tools for file system operations and command execution.

This package provides LangChain-compatible tools for:
- ls: List directory contents
- grep: Search for patterns in files
- tree: Display directory structure as a tree
- bash: Execute bash commands
- edit: Text editor for viewing and modifying files
- todo: Manage a todo list
"""

from buddycode.tools import (
    LsTool,
    GrepTool,
    TreeTool,
    BashTool,
    EditTool,
    TodoTool,
    get_file_system_tools,
)
from dotenv import load_dotenv

__version__ = "0.1.0"
__all__ = [
    "LsTool",
    "GrepTool",
    "TreeTool",
    "BashTool",
    "EditTool",
    "TodoTool",
    "get_file_system_tools",
]

load_dotenv()
def hello() -> str:
    """Legacy hello function."""
    return "Hello from buddycode!"
