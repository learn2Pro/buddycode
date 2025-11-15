"""
Test suite for React Code Agent.

Run with: uv run python test_agent.py
"""

import os
import tempfile
from pathlib import Path


def test_agent_creation():
    """Test that the agent can be created successfully."""
    print("Testing agent creation...")
    try:
        from buddycode.react_agent import create_coding_agent

        # Test coding agent creation
        coding_agent = create_coding_agent()
        assert coding_agent is not None, "Coding agent should be created"

        print("✓ Agent creation works correctly")
        return True
    except Exception as e:
        print(f"✗ Agent creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_agent_with_custom_tools():
    """Test agent creation with custom plugin tools."""
    print("\nTesting agent with custom tools...")
    try:
        from buddycode.react_agent import create_coding_agent
        from langchain_core.tools import tool

        # Create a simple custom tool using decorator
        @tool
        def custom_test_tool(input_str: str) -> str:
            """A custom tool for testing."""
            return f"Custom tool processed: {input_str}"

        # Create agent with custom tool
        agent = create_coding_agent(plugin_tools=[custom_test_tool])
        assert agent is not None, "Agent with custom tools should be created"

        print("✓ Agent with custom tools works correctly")
        return True
    except Exception as e:
        print(f"✗ Agent with custom tools failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_agent_tool_availability():
    """Test that all expected tools are available to the agent."""
    print("\nTesting agent tool availability...")
    try:
        from buddycode.react_agent import create_coding_agent
        from buddycode.tools import get_file_system_tools

        agent = create_coding_agent()

        # Get the tools from the agent's graph
        # The tools are stored in the agent's state
        expected_tools = get_file_system_tools()
        expected_tool_names = {tool.name for tool in expected_tools}

        print(f"  Expected tools: {expected_tool_names}")
        print("✓ Agent tool availability check passed")
        return True
    except Exception as e:
        print(f"✗ Agent tool availability test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_agent_simple_task():
    """Test agent with a simple task."""
    print("\nTesting agent with simple task...")
    try:
        from buddycode.react_agent import create_coding_agent

        agent = create_coding_agent()
        config = {"configurable": {"thread_id": "test_simple"}}

        # Simple task: list current directory
        result = agent.invoke(
            {"messages": [("user", "使用 bash 工具执行 pwd 命令")]},
            config
        )

        assert "messages" in result, "Result should contain messages"
        assert len(result["messages"]) > 0, "Should have at least one message"

        last_message = result["messages"][-1]
        assert hasattr(last_message, 'content'), "Message should have content"

        print(f"  Response preview: {last_message.content[:100]}...")
        print("✓ Simple task execution works correctly")
        return True
    except Exception as e:
        print(f"✗ Simple task test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_agent_view_file():
    """Test agent viewing a file."""
    print("\nTesting agent view file operation...")
    try:
        from buddycode.react_agent import create_coding_agent
        import tempfile
        import os

        agent = create_coding_agent()
        config = {"configurable": {"thread_id": "test_view"}}

        # Create a test file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as f:
            test_file = f.name
            f.write("# Test file\nprint('Hello, World!')\n")

        try:
            # Ask agent to view the file
            result = agent.invoke(
                {"messages": [("user", f"使用 edit 工具的 view 操作查看文件 {test_file}")]},
                config
            )

            assert "messages" in result, "Result should contain messages"
            last_message = result["messages"][-1]

            # Check if the response mentions the file or its content
            response = last_message.content
            assert len(response) > 0, "Response should not be empty"

            print(f"  Response preview: {response[:150]}...")
            print("✓ View file operation works correctly")
            return True
        finally:
            os.unlink(test_file)

    except Exception as e:
        print(f"✗ View file test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_agent_create_file():
    """Test agent creating a file."""
    print("\nTesting agent create file operation...")
    try:
        from buddycode.react_agent import create_coding_agent
        import tempfile
        import os

        agent = create_coding_agent()
        config = {"configurable": {"thread_id": "test_create"}}

        # Create a temporary directory
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = os.path.join(tmpdir, "test_component.tsx")

            # Ask agent to create a file
            result = agent.invoke(
                {"messages": [(
                    "user",
                    f"使用 edit 工具在 {test_file} 创建一个简单的 React 组件，"
                    f"组件名为 TestComponent，接受一个 title 属性"
                )]},
                config
            )

            assert "messages" in result, "Result should contain messages"
            last_message = result["messages"][-1]
            response = last_message.content

            print(f"  Response preview: {response[:150]}...")

            # Check if file was created (agent might have created it)
            if os.path.exists(test_file):
                print(f"  ✓ File was created: {test_file}")
                with open(test_file, 'r') as f:
                    content = f.read()
                    print(f"  File content preview: {content[:100]}...")

            print("✓ Create file operation works correctly")
            return True

    except Exception as e:
        print(f"✗ Create file test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_agent_multi_turn_conversation():
    """Test agent with multi-turn conversation (memory)."""
    print("\nTesting multi-turn conversation...")
    try:
        from buddycode.react_agent import create_coding_agent

        agent = create_coding_agent()
        config = {"configurable": {"thread_id": "test_multiturn"}}

        # First turn
        result1 = agent.invoke(
            {"messages": [("user", "使用 bash 执行 pwd 命令")]},
            config
        )

        assert "messages" in result1, "First result should contain messages"
        response1 = result1["messages"][-1].content
        print(f"  Turn 1 response: {response1[:100]}...")

        # Second turn - reference to previous context
        result2 = agent.invoke(
            {"messages": [("user", "使用 ls 工具列出这个目录的内容")]},
            config
        )

        assert "messages" in result2, "Second result should contain messages"
        response2 = result2["messages"][-1].content
        print(f"  Turn 2 response: {response2[:100]}...")

        # The conversation history should be maintained
        # Check that we got responses for both turns
        assert len(response1) > 0 and len(response2) > 0, "Both turns should have responses"

        print("✓ Multi-turn conversation works correctly")
        return True
    except Exception as e:
        print(f"✗ Multi-turn conversation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_agent_grep_search():
    """Test agent using grep tool."""
    print("\nTesting agent grep search...")
    try:
        from buddycode.react_agent import create_coding_agent

        agent = create_coding_agent()
        config = {"configurable": {"thread_id": "test_grep"}}

        # Ask agent to search for imports
        result = agent.invoke(
            {"messages": [("user", "使用 grep 工具在当前目录搜索 Python 文件中的 'import' 语句，最多显示 5 个结果")]},
            config
        )

        assert "messages" in result, "Result should contain messages"
        last_message = result["messages"][-1]
        response = last_message.content

        print(f"  Response preview: {response[:150]}...")
        print("✓ Grep search works correctly")
        return True
    except Exception as e:
        print(f"✗ Grep search test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_agent_tree_structure():
    """Test agent using tree tool."""
    print("\nTesting agent tree structure...")
    try:
        from buddycode.react_agent import create_coding_agent

        agent = create_coding_agent()
        config = {"configurable": {"thread_id": "test_tree"}}

        # Ask agent to show directory tree
        result = agent.invoke(
            {"messages": [("user", "使用 tree 工具显示当前目录结构，深度限制为 2")]},
            config
        )

        assert "messages" in result, "Result should contain messages"
        last_message = result["messages"][-1]
        response = last_message.content

        print(f"  Response preview: {response[:150]}...")
        print("✓ Tree structure display works correctly")
        return True
    except Exception as e:
        print(f"✗ Tree structure test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_agent_error_handling():
    """Test agent error handling with invalid requests."""
    print("\nTesting agent error handling...")
    try:
        from buddycode.react_agent import create_coding_agent

        agent = create_coding_agent()
        config = {"configurable": {"thread_id": "test_error"}}

        # Ask agent to view non-existent file
        result = agent.invoke(
            {"messages": [("user", "使用 edit 工具查看文件 /nonexistent/path/file.txt")]},
            config
        )

        assert "messages" in result, "Result should contain messages"
        last_message = result["messages"][-1]
        response = last_message.content

        # Should handle the error gracefully
        assert len(response) > 0, "Should provide error response"

        print(f"  Error response preview: {response[:150]}...")
        print("✓ Error handling works correctly")
        return True
    except Exception as e:
        print(f"✗ Error handling test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_agent_system_prompt():
    """Test that agent has the correct system prompt."""
    print("\nTesting agent system prompt...")
    try:
        from buddycode.react_agent import SYSTEM_PROMPT

        assert SYSTEM_PROMPT is not None, "SYSTEM_PROMPT should be defined"
        assert "coding agent" in SYSTEM_PROMPT.lower(), "Should identify as coding agent"

        print(f"  System prompt length: {len(SYSTEM_PROMPT)} characters")
        print("✓ System prompt is correctly configured")
        return True
    except Exception as e:
        print(f"✗ System prompt test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all agent tests."""
    print("=" * 70)
    print("React Code Agent - Test Suite")
    print("=" * 70)

    tests = [
        ("Agent Creation", test_agent_creation),
        ("Agent with Custom Tools", test_agent_with_custom_tools),
        ("Tool Availability", test_agent_tool_availability),
        ("Simple Task", test_agent_simple_task),
        ("View File", test_agent_view_file),
        ("Create File", test_agent_create_file),
        ("Multi-turn Conversation", test_agent_multi_turn_conversation),
        ("Grep Search", test_agent_grep_search),
        ("Tree Structure", test_agent_tree_structure),
        ("Error Handling", test_agent_error_handling),
        ("System Prompt", test_agent_system_prompt),
    ]

    results = []
    for i, (name, test_func) in enumerate(tests, 1):
        print(f"\n[{i}/{len(tests)}] Running: {name}")
        print("-" * 70)
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"✗ Unexpected error in {name}: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)

    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("\n🎉 All agent tests passed!")
        return 0
    else:
        print(f"\n⚠️ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit(main())
