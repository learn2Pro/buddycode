"""
Usage Examples for BuddyCode File System Tools

This file demonstrates various ways to use the ls, grep, and tree tools
both directly and with LangChain agents.
"""

import os
from pathlib import Path


def example_1_basic_tool_usage():
    """Example 1: Basic usage of each tool directly."""
    print("=" * 70)
    print("EXAMPLE 1: Basic Tool Usage")
    print("=" * 70)

    from buddycode.tools import LsTool, GrepTool, TreeTool

    # Initialize tools
    ls_tool = LsTool()
    grep_tool = GrepTool()
    tree_tool = TreeTool()

    # Use ls to list current directory
    print("\n1. Listing current directory:")
    print("-" * 70)
    result = ls_tool._run(path=".")
    print(result)

    # Use tree to show directory structure
    print("\n2. Directory tree (max depth 2):")
    print("-" * 70)
    result = tree_tool._run(path=".", max_depth=2)
    print(result)

    # Use grep to search for imports
    print("\n3. Searching for import statements:")
    print("-" * 70)
    result = grep_tool._run(
        pattern="^import |^from .* import",
        path="./src",
        file_pattern="*.py",
        max_results=10
    )
    print(result)


def example_2_advanced_ls():
    """Example 2: Advanced ls features."""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Advanced ls Features")
    print("=" * 70)

    from buddycode.tools import LsTool

    ls_tool = LsTool()

    # Long format listing
    print("\n1. Long format with details:")
    print("-" * 70)
    result = ls_tool._run(path=".", long_format=True)
    print(result)

    # Recursive listing
    print("\n2. Recursive listing of src:")
    print("-" * 70)
    result = ls_tool._run(path="./src", recursive=True, show_hidden=False)
    print(result)

    # Show hidden files
    print("\n3. Including hidden files:")
    print("-" * 70)
    result = ls_tool._run(path=".", show_hidden=True)
    print(result)


def example_3_advanced_grep():
    """Example 3: Advanced grep features."""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Advanced grep Features")
    print("=" * 70)

    from buddycode.tools import GrepTool

    grep_tool = GrepTool()

    # Case-insensitive search
    print("\n1. Case-insensitive search for 'tool':")
    print("-" * 70)
    result = grep_tool._run(
        pattern="tool",
        case_insensitive=True,
        file_pattern="*.py",
        max_results=5
    )
    print(result)

    # Search with context lines
    print("\n2. Search with context lines:")
    print("-" * 70)
    result = grep_tool._run(
        pattern="class.*Tool",
        context_lines=2,
        file_pattern="*.py",
        max_results=3
    )
    print(result)

    # Regex pattern search
    print("\n3. Complex regex pattern:")
    print("-" * 70)
    result = grep_tool._run(
        pattern=r"def\s+\w+\(",
        file_pattern="*.py",
        max_results=10
    )
    print(result)


def example_4_advanced_tree():
    """Example 4: Advanced tree features."""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Advanced tree Features")
    print("=" * 70)

    from buddycode.tools import TreeTool

    tree_tool = TreeTool()

    # Basic tree
    print("\n1. Basic tree structure:")
    print("-" * 70)
    result = tree_tool._run(path=".")
    print(result)

    # Directories only
    print("\n2. Directories only:")
    print("-" * 70)
    result = tree_tool._run(path=".", dirs_only=True)
    print(result)

    # Limited depth
    print("\n3. Tree with max depth 1:")
    print("-" * 70)
    result = tree_tool._run(path=".", max_depth=1)
    print(result)


def example_5_langchain_agent():
    """Example 5: Using tools with a LangChain agent."""
    print("\n" + "=" * 70)
    print("EXAMPLE 5: LangChain Agent Integration")
    print("=" * 70)

    try:
        from langchain_openai import ChatOpenAI
        from langchain.agents import initialize_agent, AgentType
        from buddycode.tools import get_file_system_tools

        # Check for API key
        if not os.getenv("OPENAI_API_KEY"):
            print("\nSkipping: OPENAI_API_KEY not set")
            print("Set your API key: export OPENAI_API_KEY='your-key-here'")
            return

        # Initialize
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        tools = get_file_system_tools()

        # Create agent
        agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True
        )

        # Test queries
        queries = [
            "List all Python files in the src directory",
            "Show me the directory tree with max depth 2",
            "Find all class definitions in Python files"
        ]

        for i, query in enumerate(queries, 1):
            print(f"\n{i}. Query: {query}")
            print("-" * 70)
            try:
                response = agent.run(query)
                print(f"Response: {response}")
            except Exception as e:
                print(f"Error: {e}")

    except ImportError as e:
        print(f"\nSkipping: Missing dependencies - {e}")
        print("Install with: uv add langchain langchain-openai")


def example_6_langgraph_agent():
    """Example 6: Using tools with LangGraph."""
    print("\n" + "=" * 70)
    print("EXAMPLE 6: LangGraph Integration")
    print("=" * 70)

    try:
        from langgraph.prebuilt import create_react_agent
        from langchain_openai import ChatOpenAI
        from buddycode.tools import get_file_system_tools

        # Check for API key
        if not os.getenv("OPENAI_API_KEY"):
            print("\nSkipping: OPENAI_API_KEY not set")
            return

        # Initialize
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        tools = get_file_system_tools()

        # Create graph
        graph = create_react_agent(llm, tools)

        # Run query
        query = "What is the structure of this project? Show me the tree."
        print(f"\nQuery: {query}")
        print("-" * 70)

        inputs = {"messages": [("user", query)]}
        for chunk in graph.stream(inputs, stream_mode="values"):
            chunk["messages"][-1].pretty_print()

    except ImportError as e:
        print(f"\nSkipping: Missing dependencies - {e}")
        print("Install with: uv add langgraph langchain-openai")


def example_7_practical_use_cases():
    """Example 7: Practical use cases."""
    print("\n" + "=" * 70)
    print("EXAMPLE 7: Practical Use Cases")
    print("=" * 70)

    from buddycode.tools import LsTool, GrepTool, TreeTool

    ls_tool = LsTool()
    grep_tool = GrepTool()
    tree_tool = TreeTool()

    print("\n1. Find all TODO comments in code:")
    print("-" * 70)
    result = grep_tool._run(
        pattern="TODO|FIXME|HACK",
        file_pattern="*.py",
        case_insensitive=True,
        context_lines=1,
        max_results=20
    )
    print(result)

    print("\n2. List all test files:")
    print("-" * 70)
    result = grep_tool._run(
        pattern="test_",
        file_pattern="*.py",
        max_results=20
    )
    print(result)

    print("\n3. Find all class definitions:")
    print("-" * 70)
    result = grep_tool._run(
        pattern="^class\s+\w+",
        file_pattern="*.py",
        max_results=20
    )
    print(result)

    print("\n4. Project overview (tree + Python file count):")
    print("-" * 70)
    tree_result = tree_tool._run(path=".", max_depth=3)
    print(tree_result)


def example_8_error_handling():
    """Example 8: Error handling and edge cases."""
    print("\n" + "=" * 70)
    print("EXAMPLE 8: Error Handling")
    print("=" * 70)

    from buddycode.tools import LsTool, GrepTool, TreeTool

    ls_tool = LsTool()
    grep_tool = GrepTool()
    tree_tool = TreeTool()

    # Non-existent path
    print("\n1. Non-existent path:")
    print("-" * 70)
    result = ls_tool._run(path="/nonexistent/path")
    print(result)

    # Invalid regex
    print("\n2. Invalid regex pattern:")
    print("-" * 70)
    result = grep_tool._run(pattern="[invalid(regex")
    print(result)

    # File instead of directory for tree
    print("\n3. File path for tree (should error):")
    print("-" * 70)
    result = tree_tool._run(path="./README.md")
    print(result)

    # Empty directory
    print("\n4. Empty directory:")
    print("-" * 70)
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        result = ls_tool._run(path=tmpdir)
        print(result)


def example_9_combined_workflow():
    """Example 9: Combined workflow - analyze a project."""
    print("\n" + "=" * 70)
    print("EXAMPLE 9: Combined Workflow - Project Analysis")
    print("=" * 70)

    from buddycode.tools import LsTool, GrepTool, TreeTool

    ls_tool = LsTool()
    grep_tool = GrepTool()
    tree_tool = TreeTool()

    print("\n📁 Step 1: Overview - Directory Tree")
    print("-" * 70)
    tree_result = tree_tool._run(path=".", max_depth=2)
    print(tree_result)

    print("\n📝 Step 2: Find Python Files")
    print("-" * 70)
    ls_result = ls_tool._run(path="./src", recursive=True)
    print(ls_result)

    print("\n🔍 Step 3: Analyze Imports")
    print("-" * 70)
    grep_result = grep_tool._run(
        pattern="^from |^import ",
        path="./src",
        file_pattern="*.py",
        max_results=20
    )
    print(grep_result)

    print("\n🏗️ Step 4: Find All Classes")
    print("-" * 70)
    grep_result = grep_tool._run(
        pattern="^class ",
        path="./src",
        file_pattern="*.py",
        max_results=20
    )
    print(grep_result)

    print("\n✅ Step 5: Project Summary")
    print("-" * 70)
    print("Analysis complete! This workflow demonstrates:")
    print("  - Directory structure visualization")
    print("  - File discovery")
    print("  - Code pattern analysis")
    print("  - Dependency tracking")


def example_10_bash_tool():
    """Example 10: Using BashTool for command execution."""
    print("\n" + "=" * 70)
    print("EXAMPLE 10: BashTool - Command Execution")
    print("=" * 70)

    from buddycode.tools import BashTool

    bash_tool = BashTool()

    print("\n1. Simple command - echo:")
    print("-" * 70)
    result = bash_tool._run(command="echo 'Hello from BashTool!'")
    print(result)

    print("\n2. System information:")
    print("-" * 70)
    result = bash_tool._run(command="uname -s")
    print(result)

    print("\n3. List Python files:")
    print("-" * 70)
    result = bash_tool._run(command="find . -name '*.py' -type f | head -5")
    print(result)

    print("\n4. Count lines of code:")
    print("-" * 70)
    result = bash_tool._run(command="find ./src -name '*.py' -exec wc -l {} + | tail -1")
    print(result)

    print("\n5. Git status (if in git repo):")
    print("-" * 70)
    result = bash_tool._run(command="git status --short")
    print(result)

    print("\n6. Python version:")
    print("-" * 70)
    result = bash_tool._run(command="python --version")
    print(result)

    print("\n7. Working directory test:")
    print("-" * 70)
    result = bash_tool._run(command="pwd", working_dir="./src")
    print(result)

    print("\n8. Timeout test (command that completes quickly):")
    print("-" * 70)
    result = bash_tool._run(command="sleep 1 && echo 'Done!'", timeout=5)
    print(result)

    print("\n9. Command with stderr (intentional warning):")
    print("-" * 70)
    result = bash_tool._run(command="ls /nonexistent 2>&1 || echo 'Expected error'")
    print(result)

    print("\n10. Environment variables:")
    print("-" * 70)
    result = bash_tool._run(command="echo $HOME")
    print(result)


def example_11_bash_integration():
    """Example 11: BashTool integrated with other tools."""
    print("\n" + "=" * 70)
    print("EXAMPLE 11: BashTool Integration - DevOps Workflow")
    print("=" * 70)

    from buddycode.tools import BashTool, TreeTool, GrepTool

    bash = BashTool()
    tree = TreeTool()
    grep = GrepTool()

    print("\n📁 Step 1: Show project structure")
    print("-" * 70)
    result = tree._run(path=".", max_depth=2)
    print(result)

    print("\n🔍 Step 2: Find Python files")
    print("-" * 70)
    result = bash._run(command="find . -name '*.py' -type f | wc -l")
    print(result)

    print("\n📊 Step 3: Code statistics")
    print("-" * 70)
    result = bash._run(command="find ./src -name '*.py' -exec wc -l {} + 2>/dev/null | tail -1 || echo 'No files found'")
    print(result)

    print("\n🔎 Step 4: Find TODOs")
    print("-" * 70)
    result = grep._run(
        pattern="TODO|FIXME",
        file_pattern="*.py",
        max_results=5
    )
    print(result)

    print("\n✅ Step 5: Check if tests exist")
    print("-" * 70)
    result = bash._run(command="test -f test_tools.py && echo 'Tests found' || echo 'No tests'")
    print(result)

    print("\n📝 Step 6: Git information (if available)")
    print("-" * 70)
    result = bash._run(command="git log --oneline -5 2>/dev/null || echo 'Not a git repository'")
    print(result)


def example_12_edit_tool():
    """Example 12: Using EditTool for file operations."""
    print("\n" + "=" * 70)
    print("EXAMPLE 12: EditTool - Text Editing Operations")
    print("=" * 70)

    from buddycode.tools import EditTool
    import tempfile
    import os

    edit_tool = EditTool()

    # Create a temporary directory for demo
    with tempfile.TemporaryDirectory() as tmpdir:
        demo_file = os.path.join(tmpdir, "demo.py")

        print("\n1. CREATE operation - Create a new file:")
        print("-" * 70)
        result = edit_tool._run(
            operation="create",
            file_path=demo_file,
            content="""# Demo Python Script
import os
import sys

def hello(name):
    print(f"Hello, {name}!")

def main():
    hello("World")
"""
        )
        print(result)

        print("\n2. VIEW operation - View entire file:")
        print("-" * 70)
        result = edit_tool._run(
            operation="view",
            file_path=demo_file
        )
        print(result)

        print("\n3. VIEW operation - View specific line range:")
        print("-" * 70)
        result = edit_tool._run(
            operation="view",
            file_path=demo_file,
            start_line=1,
            end_line=5
        )
        print(result)

        print("\n4. INSERT operation - Add new function:")
        print("-" * 70)
        result = edit_tool._run(
            operation="insert",
            file_path=demo_file,
            line_number=8,
            content="""\ndef goodbye(name):
    print(f"Goodbye, {name}!")
"""
        )
        print(result)

        print("\n5. VIEW after INSERT:")
        print("-" * 70)
        result = edit_tool._run(
            operation="view",
            file_path=demo_file
        )
        print(result)

        print("\n6. STR_REPLACE operation - Update greeting:")
        print("-" * 70)
        result = edit_tool._run(
            operation="str_replace",
            file_path=demo_file,
            old_str='print(f"Hello, {name}!")',
            new_str='print(f"Greetings, {name}!")'
        )
        print(result)

        print("\n7. VIEW after STR_REPLACE:")
        print("-" * 70)
        result = edit_tool._run(
            operation="view",
            file_path=demo_file,
            start_line=4,
            end_line=6
        )
        print(result)

        print("\n8. INSERT at beginning - Add import:")
        print("-" * 70)
        result = edit_tool._run(
            operation="insert",
            file_path=demo_file,
            line_number=3,
            content="import json\n"
        )
        print(result)

        print("\n9. Final VIEW:")
        print("-" * 70)
        result = edit_tool._run(
            operation="view",
            file_path=demo_file
        )
        print(result)


def example_13_edit_workflow():
    """Example 13: Complete editing workflow with EditTool."""
    print("\n" + "=" * 70)
    print("EXAMPLE 13: EditTool - Complete Workflow")
    print("=" * 70)

    from buddycode.tools import EditTool, GrepTool
    import tempfile
    import os

    edit = EditTool()
    grep = GrepTool()

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a config file
        config_file = os.path.join(tmpdir, "config.py")

        print("\n📝 Step 1: Create configuration file")
        print("-" * 70)
        result = edit._run(
            operation="create",
            file_path=config_file,
            content="""# Application Configuration

DEBUG = True
PORT = 8000
HOST = "localhost"
DATABASE_URL = "sqlite:///dev.db"

# API Settings
API_VERSION = "v1"
API_TIMEOUT = 30
"""
        )
        print(result)

        print("\n👀 Step 2: View the configuration")
        print("-" * 70)
        result = edit._run(operation="view", file_path=config_file)
        print(result)

        print("\n🔄 Step 3: Update DEBUG to False")
        print("-" * 70)
        result = edit._run(
            operation="str_replace",
            file_path=config_file,
            old_str="DEBUG = True",
            new_str="DEBUG = False"
        )
        print(result)

        print("\n➕ Step 4: Add new configuration section")
        print("-" * 70)
        result = edit._run(
            operation="insert",
            file_path=config_file,
            line_number=11,
            content="""\n# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FILE = "app.log"
"""
        )
        print(result)

        print("\n🔍 Step 5: Search for specific settings")
        print("-" * 70)
        result = grep._run(
            pattern="API_",
            path=config_file,
            max_results=10
        )
        print(result)

        print("\n🔄 Step 6: Update API timeout")
        print("-" * 70)
        result = edit._run(
            operation="str_replace",
            file_path=config_file,
            old_str="API_TIMEOUT = 30",
            new_str="API_TIMEOUT = 60"
        )
        print(result)

        print("\n✅ Step 7: Final configuration view")
        print("-" * 70)
        result = edit._run(operation="view", file_path=config_file)
        print(result)

        print("\n📊 Summary:")
        print("-" * 70)
        print("Completed workflow:")
        print("  ✓ Created configuration file")
        print("  ✓ Changed DEBUG mode")
        print("  ✓ Added logging configuration")
        print("  ✓ Updated API timeout")
        print("  ✓ Verified all changes")


def main():
    """Run all examples."""
    print("\n" + "=" * 70)
    print("BuddyCode File System Tools - Examples")
    print("=" * 70)

    examples = [
        ("Basic Tool Usage", example_1_basic_tool_usage),
        ("Advanced ls", example_2_advanced_ls),
        ("Advanced grep", example_3_advanced_grep),
        ("Advanced tree", example_4_advanced_tree),
        ("LangChain Agent", example_5_langchain_agent),
        ("LangGraph", example_6_langgraph_agent),
        ("Practical Use Cases", example_7_practical_use_cases),
        ("Error Handling", example_8_error_handling),
        ("Combined Workflow", example_9_combined_workflow),
        ("BashTool", example_10_bash_tool),
        ("BashTool Integration", example_11_bash_integration),
        ("EditTool", example_12_edit_tool),
        ("EditTool Workflow", example_13_edit_workflow),
    ]

    for i, (name, func) in enumerate(examples, 1):
        try:
            func()
        except Exception as e:
            print(f"\n⚠️ Example {i} ({name}) failed: {e}")

        # Pause between examples
        if i < len(examples):
            input("\n\nPress Enter to continue to next example...")

    print("\n" + "=" * 70)
    print("All examples completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()
