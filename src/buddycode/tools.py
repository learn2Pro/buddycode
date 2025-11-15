"""
LangChain Tools for File System Operations and Command Execution

This module provides LangChain-compatible tools for common file system operations:
- ls: List directory contents
- grep: Search for patterns in files
- tree: Display directory structure as a tree
- bash: Execute bash commands
- edit: Text editor for viewing and modifying files
- todo: Manage a todo list
"""

from enum import Enum
import os
import re
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Any
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class LsInput(BaseModel):
    """Input schema for ls tool."""
    path: str = Field(default=".", description="Directory path to list (default: current directory)")
    show_hidden: bool = Field(default=False, description="Show hidden files (starting with .)")
    long_format: bool = Field(default=False, description="Show detailed information (size, permissions, modified time)")
    recursive: bool = Field(default=False, description="List subdirectories recursively")


class LsTool(BaseTool):
    """Tool for listing directory contents."""

    name: str = "ls"
    description: str = "List directory contents. Useful for exploring file system structure and finding files."
    args_schema: type[BaseModel] = LsInput

    def _run(
        self,
        path: str = ".",
        show_hidden: bool = False,
        long_format: bool = False,
        recursive: bool = False
    ) -> str:
        """Execute ls operation."""
        try:
            target_path = Path(path).expanduser().resolve()

            if not target_path.exists():
                return f"Error: Path '{path}' does not exist"

            if not target_path.is_dir():
                return f"Error: Path '{path}' is not a directory"

            results = []

            def list_directory(dir_path: Path, prefix: str = "") -> None:
                """List contents of a directory."""
                try:
                    items = sorted(dir_path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))

                    for item in items:
                        # Skip hidden files if not requested
                        if not show_hidden and item.name.startswith('.'):
                            continue

                        if long_format:
                            # Show detailed information
                            stat = item.stat()
                            size = stat.st_size
                            modified = stat.st_mtime
                            is_dir = item.is_dir()
                            perms = oct(stat.st_mode)[-3:]

                            from datetime import datetime
                            mod_time = datetime.fromtimestamp(modified).strftime("%Y-%m-%d %H:%M:%S")

                            item_type = "DIR" if is_dir else "FILE"
                            results.append(f"{prefix}{perms} {item_type:4} {size:>10} {mod_time} {item.name}")
                        else:
                            # Simple format
                            suffix = "/" if item.is_dir() else ""
                            results.append(f"{prefix}{item.name}{suffix}")

                        # Recurse into subdirectories if requested
                        if recursive and item.is_dir():
                            list_directory(item, prefix=prefix + "  ")

                except PermissionError:
                    results.append(f"{prefix}[Permission Denied]")

            list_directory(target_path)

            if not results:
                return f"Directory '{path}' is empty"

            header = f"Contents of '{path}':\n" + ("-" * 50) + "\n"
            return header + "\n".join(results)

        except Exception as e:
            return f"Error: {str(e)}"


class GrepInput(BaseModel):
    """Input schema for grep tool."""
    pattern: str = Field(description="Regular expression pattern to search for")
    path: str = Field(default=".", description="File or directory path to search in")
    file_pattern: Optional[str] = Field(default=None, description="Filter files by glob pattern (e.g., '*.py', '*.txt')")
    case_insensitive: bool = Field(default=False, description="Perform case-insensitive search")
    context_lines: int = Field(default=0, description="Number of context lines to show before and after match")
    max_results: int = Field(default=100, description="Maximum number of results to return")


class GrepTool(BaseTool):
    """Tool for searching text patterns in files."""

    name: str = "grep"
    description: str = "Search for text patterns in files using regular expressions. Useful for finding specific code or content."
    args_schema: type[BaseModel] = GrepInput

    def _run(
        self,
        pattern: str,
        path: str = ".",
        file_pattern: Optional[str] = None,
        case_insensitive: bool = False,
        context_lines: int = 0,
        max_results: int = 100
    ) -> str:
        """Execute grep operation."""
        try:
            target_path = Path(path).expanduser().resolve()

            if not target_path.exists():
                return f"Error: Path '{path}' does not exist"

            # Compile regex pattern
            flags = re.IGNORECASE if case_insensitive else 0
            try:
                regex = re.compile(pattern, flags)
            except re.error as e:
                return f"Error: Invalid regex pattern: {e}"

            results = []
            total_matches = 0

            def search_file(file_path: Path) -> None:
                """Search for pattern in a single file."""
                nonlocal total_matches

                if total_matches >= max_results:
                    return

                try:
                    # Skip binary files
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()

                    matches = []
                    for line_num, line in enumerate(lines, 1):
                        if regex.search(line):
                            matches.append((line_num, line.rstrip()))

                    if matches:
                        results.append(f"\n{file_path}:")
                        for line_num, line in matches:
                            if total_matches >= max_results:
                                break

                            results.append(f"  {line_num:4d}: {line}")

                            # Add context lines
                            if context_lines > 0:
                                # Before context
                                for i in range(max(0, line_num - context_lines - 1), line_num - 1):
                                    if i < len(lines):
                                        results.append(f"  {i+1:4d}- {lines[i].rstrip()}")

                                # After context
                                for i in range(line_num, min(len(lines), line_num + context_lines)):
                                    results.append(f"  {i+1:4d}- {lines[i].rstrip()}")

                            total_matches += 1

                except (UnicodeDecodeError, PermissionError):
                    pass  # Skip files that can't be read

            def search_directory(dir_path: Path) -> None:
                """Recursively search directory."""
                try:
                    for item in dir_path.iterdir():
                        if total_matches >= max_results:
                            break

                        # Skip hidden files and common ignore patterns
                        if item.name.startswith('.') or item.name in ['node_modules', '__pycache__', 'venv', '.git']:
                            continue

                        if item.is_file():
                            # Check file pattern filter
                            if file_pattern:
                                if not item.match(file_pattern):
                                    continue
                            search_file(item)
                        elif item.is_dir():
                            search_directory(item)

                except PermissionError:
                    pass

            # Determine if searching file or directory
            if target_path.is_file():
                search_file(target_path)
            else:
                search_directory(target_path)

            if not results:
                return f"No matches found for pattern '{pattern}'"

            header = f"Search results for pattern '{pattern}':\n" + ("=" * 50)
            footer = ""
            if total_matches >= max_results:
                footer = f"\n\n(Showing first {max_results} matches, more results may exist)"

            return header + "".join(results) + footer

        except Exception as e:
            return f"Error: {str(e)}"


class TreeInput(BaseModel):
    """Input schema for tree tool."""
    path: str = Field(default=".", description="Directory path to display as tree")
    max_depth: Optional[int] = Field(default=None, description="Maximum depth to traverse (None for unlimited)")
    show_hidden: bool = Field(default=False, description="Show hidden files and directories")
    dirs_only: bool = Field(default=False, description="Show only directories")


class TreeTool(BaseTool):
    """Tool for displaying directory structure as a tree."""

    name: str = "tree"
    description: str = "Display directory structure as a tree. Useful for understanding project organization."
    args_schema: type[BaseModel] = TreeInput

    def _run(
        self,
        path: str = ".",
        max_depth: Optional[int] = None,
        show_hidden: bool = False,
        dirs_only: bool = False
    ) -> str:
        """Execute tree operation."""
        try:
            target_path = Path(path).expanduser().resolve()

            if not target_path.exists():
                return f"Error: Path '{path}' does not exist"

            if not target_path.is_dir():
                return f"Error: Path '{path}' is not a directory"

            results = [str(target_path)]
            dir_count = 0
            file_count = 0

            def build_tree(dir_path: Path, prefix: str = "", depth: int = 0) -> None:
                """Recursively build tree structure."""
                nonlocal dir_count, file_count

                if max_depth is not None and depth >= max_depth:
                    return

                try:
                    items = sorted(dir_path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))

                    # Filter items
                    if not show_hidden:
                        items = [item for item in items if not item.name.startswith('.')]

                    if dirs_only:
                        items = [item for item in items if item.is_dir()]

                    # Skip common ignored directories
                    items = [item for item in items if item.name not in ['__pycache__', 'node_modules', '.git']]

                    for i, item in enumerate(items):
                        is_last = i == len(items) - 1
                        current_prefix = "└── " if is_last else "├── "
                        next_prefix = "    " if is_last else "│   "

                        if item.is_dir():
                            results.append(f"{prefix}{current_prefix}{item.name}/")
                            dir_count += 1
                            build_tree(item, prefix + next_prefix, depth + 1)
                        else:
                            results.append(f"{prefix}{current_prefix}{item.name}")
                            file_count += 1

                except PermissionError:
                    results.append(f"{prefix}[Permission Denied]")

            build_tree(target_path)

            summary = f"\n\n{dir_count} directories"
            if not dirs_only:
                summary += f", {file_count} files"

            return "\n".join(results) + summary

        except Exception as e:
            return f"Error: {str(e)}"


class BashInput(BaseModel):
    """Input schema for bash tool."""
    command: str = Field(description="The bash command to execute")
    working_dir: Optional[str] = Field(default=None, description="Working directory for command execution (default: current directory)")
    timeout: int = Field(default=30, description="Command timeout in seconds (default: 30)")
    capture_stderr: bool = Field(default=True, description="Capture stderr along with stdout")


class BashTool(BaseTool):
    """Tool for executing bash commands.

    WARNING: This tool executes arbitrary bash commands and should be used with caution.
    Only use this in trusted environments and validate inputs carefully.
    """

    name: str = "bash"
    description: str = (
        "Execute bash commands and return the output. Useful for running system commands, "
        "scripts, or any command-line operations. Returns stdout (and optionally stderr). "
        "Use with caution as this executes arbitrary commands on the system."
    )
    args_schema: type[BaseModel] = BashInput

    def _run(
        self,
        command: str,
        working_dir: Optional[str] = None,
        timeout: int = 30,
        capture_stderr: bool = True
    ) -> str:
        """Execute bash command."""
        try:
            # Validate timeout
            if timeout <= 0 or timeout > 300:
                return "Error: Timeout must be between 1 and 300 seconds"

            # Determine working directory
            if working_dir:
                work_path = Path(working_dir).expanduser().resolve()
                if not work_path.exists():
                    return f"Error: Working directory '{working_dir}' does not exist"
                if not work_path.is_dir():
                    return f"Error: Working directory '{working_dir}' is not a directory"
                cwd = str(work_path)
            else:
                cwd = os.getcwd()

            # Execute command
            try:
                result = subprocess.run(
                    command,
                    shell=True,
                    cwd=cwd,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    env=os.environ.copy()
                )

                # Build output
                output_parts = []

                # Add stdout
                if result.stdout:
                    output_parts.append("STDOUT:\n" + result.stdout.rstrip())

                # Add stderr if requested and present
                if capture_stderr and result.stderr:
                    if output_parts:
                        output_parts.append("")  # Empty line separator
                    output_parts.append("STDERR:\n" + result.stderr.rstrip())

                # Add return code
                if output_parts:
                    output_parts.append("")  # Empty line separator
                output_parts.append(f"Exit Code: {result.returncode}")

                # If no output at all
                if not result.stdout and not (capture_stderr and result.stderr):
                    if result.returncode == 0:
                        return f"Command completed successfully (no output)\nExit Code: 0"
                    else:
                        return f"Command failed with no output\nExit Code: {result.returncode}"

                return "\n".join(output_parts)

            except subprocess.TimeoutExpired:
                return f"Error: Command timed out after {timeout} seconds"

            except FileNotFoundError:
                return f"Error: Command not found or invalid shell command"

        except Exception as e:
            return f"Error: {str(e)}"


class EditInput(BaseModel):
    """Input schema for edit tool."""
    operation: str = Field(description="Operation to perform: 'view', 'create', 'insert', or 'str_replace'")
    file_path: str = Field(description="Path to the file")
    content: Optional[str] = Field(default=None, description="Content for create/insert operations")
    line_number: Optional[int] = Field(default=None, description="Line number for insert operation (1-based)")
    start_line: Optional[int] = Field(default=None, description="Start line for view operation (1-based, inclusive)")
    end_line: Optional[int] = Field(default=None, description="End line for view operation (1-based, inclusive)")
    old_str: Optional[str] = Field(default=None, description="String to replace in str_replace operation")
    new_str: Optional[str] = Field(default=None, description="Replacement string in str_replace operation")


class EditTool(BaseTool):
    """Tool for viewing and editing text files.

    Supports four operations:
    - view: Read file contents (optionally with line range)
    - create: Create a new file with content
    - insert: Insert text at a specific line number
    - str_replace: Replace all occurrences of a string
    """

    name: str = "text_editor"
    description: str = (
        "Text editor for viewing and modifying files. Supports four operations: "
        "'view' (read file, optionally with line range), "
        "'create' (create new file), "
        "'insert' (insert text at line number), "
        "'str_replace' (replace string throughout file). "
        "Always use view before editing to see current content."
    )
    args_schema: type[BaseModel] = EditInput

    def _run(
        self,
        operation: str,
        file_path: str,
        content: Optional[str] = None,
        line_number: Optional[int] = None,
        start_line: Optional[int] = None,
        end_line: Optional[int] = None,
        old_str: Optional[str] = None,
        new_str: Optional[str] = None
    ) -> str:
        """Execute edit operation."""
        try:
            path = Path(file_path).expanduser().resolve()

            if operation == "view":
                return self._view(path, start_line, end_line)
            elif operation == "create":
                return self._create(path, content)
            elif operation == "insert":
                return self._insert(path, line_number, content)
            elif operation == "str_replace":
                return self._str_replace(path, old_str, new_str)
            else:
                return f"Error: Unknown operation '{operation}'. Must be 'view', 'create', 'insert', or 'str_replace'"

        except Exception as e:
            return f"Error: {str(e)}"

    def _view(self, path: Path, start_line: Optional[int], end_line: Optional[int]) -> str:
        """View file contents."""
        try:
            if not path.exists():
                return f"Error: File '{path}' does not exist"

            if path.is_dir():
                return f"Error: '{path}' is a directory, not a file"

            # Read file
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            if not lines:
                return f"File '{path}' is empty (0 lines)"

            total_lines = len(lines)

            # Determine line range
            if start_line is None:
                start_line = 1
            if end_line is None:
                end_line = total_lines

            # Validate line numbers
            if start_line < 1:
                return f"Error: start_line must be >= 1 (got {start_line})"
            if end_line < start_line:
                return f"Error: end_line ({end_line}) must be >= start_line ({start_line})"
            if start_line > total_lines:
                return f"Error: start_line ({start_line}) exceeds file length ({total_lines} lines)"

            # Adjust end_line if it exceeds file length
            end_line = min(end_line, total_lines)

            # Build output
            result = [f"File: {path} (lines {start_line}-{end_line} of {total_lines})", "=" * 70]

            for i in range(start_line - 1, end_line):
                line_num = i + 1
                line_content = lines[i].rstrip('\n')
                result.append(f"{line_num:4d} | {line_content}")

            return "\n".join(result)

        except UnicodeDecodeError:
            return f"Error: File '{path}' is not a text file (binary content detected)"
        except PermissionError:
            return f"Error: Permission denied reading '{path}'"

    def _create(self, path: Path, content: Optional[str]) -> str:
        """Create a new file."""
        try:
            if content is None:
                return "Error: 'content' parameter is required for create operation"

            if path.exists():
                return f"Error: File '{path}' already exists. Use str_replace or insert to modify existing files."

            # Create parent directories if they don't exist
            path.parent.mkdir(parents=True, exist_ok=True)

            # Write file
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)

            # Count lines for confirmation
            lines = content.split('\n')
            line_count = len(lines)

            return f"Success: Created '{path}' with {line_count} line{'s' if line_count != 1 else ''}"

        except PermissionError:
            return f"Error: Permission denied writing to '{path}'"

    def _insert(self, path: Path, line_number: Optional[int], content: Optional[str]) -> str:
        """Insert text at a specific line number."""
        try:
            if content is None:
                return "Error: 'content' parameter is required for insert operation"
            if line_number is None:
                return "Error: 'line_number' parameter is required for insert operation"

            if not path.exists():
                return f"Error: File '{path}' does not exist. Use 'create' operation for new files."

            if path.is_dir():
                return f"Error: '{path}' is a directory, not a file"

            # Read existing content
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            total_lines = len(lines)

            # Validate line number (1-based, can be total_lines + 1 to append)
            if line_number < 1:
                return f"Error: line_number must be >= 1 (got {line_number})"
            if line_number > total_lines + 1:
                return f"Error: line_number ({line_number}) exceeds file length + 1 ({total_lines + 1} lines)"

            # Insert content
            # If content doesn't end with newline, add one
            if not content.endswith('\n'):
                content += '\n'

            # Insert at position (line_number - 1 is the index)
            insert_pos = line_number - 1
            lines.insert(insert_pos, content)

            # Write back
            with open(path, 'w', encoding='utf-8') as f:
                f.writelines(lines)

            new_line_count = len(lines)
            return f"Success: Inserted content at line {line_number} in '{path}' (now {new_line_count} lines)"

        except UnicodeDecodeError:
            return f"Error: File '{path}' is not a text file (binary content detected)"
        except PermissionError:
            return f"Error: Permission denied modifying '{path}'"

    def _str_replace(self, path: Path, old_str: Optional[str], new_str: Optional[str]) -> str:
        """Replace all occurrences of a string."""
        try:
            if old_str is None:
                return "Error: 'old_str' parameter is required for str_replace operation"
            if new_str is None:
                return "Error: 'new_str' parameter is required for str_replace operation"

            if not path.exists():
                return f"Error: File '{path}' does not exist"

            if path.is_dir():
                return f"Error: '{path}' is a directory, not a file"

            # Read file
            with open(path, 'r', encoding='utf-8') as f:
                original_content = f.read()

            # Check if old_str exists
            if old_str not in original_content:
                return f"Error: String '{old_str}' not found in '{path}'"

            # Count occurrences
            count = original_content.count(old_str)

            # Perform replacement
            new_content = original_content.replace(old_str, new_str)

            # Write back
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            return f"Success: Replaced {count} occurrence{'s' if count != 1 else ''} of '{old_str}' with '{new_str}' in '{path}'"

        except UnicodeDecodeError:
            return f"Error: File '{path}' is not a text file (binary content detected)"
        except PermissionError:
            return f"Error: Permission denied modifying '{path}'"


class TodoStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"

class TodoPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TodoItem(BaseModel):
    """Representation of a TODO item."""

    id: int = Field(..., ge=0)
    content: str = Field(..., min_length=1)
    priority: TodoPriority = Field(default=TodoPriority.medium)
    status: TodoStatus = Field(default=TodoStatus.pending)

class TodoInput(BaseModel):
    """Input schema for todo tool."""
    operation: str = Field(description="Operation to perform: 'write' or 'list'")
    items: Optional[List[TodoItem]] = Field(default=None, description="List of todo items for 'write' operation")


class TodoTool(BaseTool):
    """Tool for managing a simple todo list."""

    name: str = "todo"
    description: str = (
        "Manage a todo list. Operations: "
        "'write' (init/update a todo plan), 'list' (show all the todos), "
        "Useful for tracking tasks and action items."
    )
    args_schema: type[BaseModel] = TodoInput

    # Class variable to store todos across invocations
    _todos: List[TodoItem] = []

    def _run(
        self,
        operation: str,
        items: List[TodoItem],
    ) -> str:
        """Execute todo operation."""
        try:
            if operation == "write":
                if not items:
                    return "Error: 'item' is required for 'add' operation"

                self._todos = items
                return f"Success: write #{len(self._todos)} todos!"

            elif operation == "list":
                if not self._todos:
                    return "Todo list is empty"

                result = ["Todo List:", "-" * 50]
                for i, todo in enumerate(self._todos, 1):
                    status = "✓" if todo.status == TodoStatus.completed else " "
                    result.append(f"{i}. [{status}] {todo['text']}")

                completed = sum(1 for t in self._todos if t.status == TodoStatus.completed)
                total = len(self._todos)
                result.append("-" * 50)
                result.append(f"Total: {total} items ({completed} completed, {total - completed} pending)")

                return "\n".join(result)

            else:
                return f"Error: Unknown operation '{operation}'. Valid operations: add, list, complete, remove, clear"

        except Exception as e:
            return f"Error: {str(e)}"


# Convenience function to get all tools
def get_file_system_tools() -> List[BaseTool]:
    """
    Get a list of all file system tools.

    Returns:
        List of BaseTool instances (LsTool, GrepTool, TreeTool, BashTool, EditTool, TodoTool)
    """
    return [LsTool(), GrepTool(), TreeTool(), BashTool(), EditTool(), TodoTool()]
