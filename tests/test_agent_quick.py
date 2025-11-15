"""
Quick tests for React Code Agent (without LLM calls).

Run with: uv run python test_agent_quick.py
"""


def test_imports():
    """Test that all agent modules can be imported."""
    print("Testing imports...")
    try:
        from buddycode.react_agent import (
            create_coding_agent,
            SYSTEM_PROMPT
        )
        from buddycode.chat_model import init_chat_model
        from buddycode.tools import get_file_system_tools

        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_system_prompt():
    """Test system prompt configuration."""
    print("\nTesting system prompt...")
    try:
        from buddycode.react_agent import SYSTEM_PROMPT

        assert SYSTEM_PROMPT is not None, "SYSTEM_PROMPT should exist"
        assert len(SYSTEM_PROMPT) > 100, "SYSTEM_PROMPT should be substantial"
        assert "agent" in SYSTEM_PROMPT.lower(), "Should identify as agent"

        print(f"  SYSTEM_PROMPT length: {len(SYSTEM_PROMPT)} characters")
        print("✓ System prompt configuration is valid")
        return True
    except Exception as e:
        print(f"✗ System prompt test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_tools_available():
    """Test that tools are available."""
    print("\nTesting tools availability...")
    try:
        from buddycode.tools import get_file_system_tools

        tools = get_file_system_tools()
        assert len(tools) == 6, f"Should have 6 tools, got {len(tools)}"

        tool_names = [tool.name for tool in tools]
        expected_names = {'ls', 'grep', 'tree', 'bash', 'text_editor', 'todo'}

        assert set(tool_names) == expected_names, f"Tool names mismatch: {tool_names} != {expected_names}"

        print(f"  Tools available: {tool_names}")
        print("✓ All expected tools are available")
        return True
    except Exception as e:
        print(f"✗ Tools availability test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_agent_creation():
    """Test agent creation (without invoking)."""
    print("\nTesting agent creation...")
    try:
        from buddycode.react_agent import create_coding_agent

        # Test coding agent creation (with memory by default)
        coding_agent = create_coding_agent()
        assert coding_agent is not None, "Coding agent should be created"
        print("  ✓ Coding agent created (with built-in memory)")

        print("✓ Agent creation works correctly")
        return True
    except Exception as e:
        print(f"✗ Agent creation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_agent_with_plugin_tools():
    """Test agent creation with custom plugin tools."""
    print("\nTesting agent with plugin tools...")
    try:
        from buddycode.react_agent import create_coding_agent
        from langchain_core.tools import tool

        # Create a dummy tool using decorator
        @tool
        def dummy_tool(input_str: str) -> str:
            """A dummy tool for testing."""
            return f"Processed: {input_str}"

        # Create agent with plugin tool
        agent = create_coding_agent(plugin_tools=[dummy_tool])
        assert agent is not None, "Agent with plugin tools should be created"

        print("  ✓ Agent created with 1 plugin tool")
        print("✓ Plugin tools integration works")
        return True
    except Exception as e:
        print(f"✗ Plugin tools test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_chat_model_creation():
    """Test chat model creation."""
    print("\nTesting chat model creation...")
    try:
        from buddycode.chat_model import init_chat_model

        model = init_chat_model()
        assert model is not None, "Chat model should be created"

        # Check model configuration
        assert hasattr(model, 'model_name') or hasattr(model, 'model'), "Model should have model name"

        print("  ✓ Chat model created successfully")
        print("✓ Chat model initialization works")
        return True
    except Exception as e:
        print(f"✗ Chat model test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_edit_tool_operations():
    """Test EditTool operations."""
    print("\nTesting EditTool operations...")
    try:
        from buddycode.tools import EditTool
        import tempfile
        import os

        edit = EditTool()

        # Create a test file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            test_file = f.name
            f.write("Line 1\nLine 2\nLine 3\n")

        try:
            # Test view
            result = edit._run(operation="view", file_path=test_file)
            assert "Line 1" in result, "View should show file content"
            assert "|" in result, "View should show line numbers"
            print("  ✓ View operation works")

            # Test str_replace
            result = edit._run(
                operation="str_replace",
                file_path=test_file,
                old_str="Line 1",
                new_str="Modified Line 1"
            )
            assert "Success" in result, "Replace should succeed"
            print("  ✓ Replace operation works")

            # Verify replacement
            result = edit._run(operation="view", file_path=test_file)
            assert "Modified Line 1" in result, "File should be modified"
            print("  ✓ Replacement verified")

            print("✓ EditTool operations work correctly")
            return True
        finally:
            os.unlink(test_file)

    except Exception as e:
        print(f"✗ EditTool test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all quick tests."""
    print("=" * 70)
    print("React Code Agent - Quick Test Suite (No LLM calls)")
    print("=" * 70)

    tests = [
        ("Imports", test_imports),
        ("System Prompt", test_system_prompt),
        ("Tools Availability", test_tools_available),
        ("Agent Creation", test_agent_creation),
        ("Plugin Tools", test_agent_with_plugin_tools),
        ("Chat Model", test_chat_model_creation),
        ("EditTool Operations", test_edit_tool_operations),
    ]

    results = []
    for i, (name, test_func) in enumerate(tests, 1):
        print(f"\n[{i}/{len(tests)}] {name}")
        print("-" * 70)
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
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
        print("\n🎉 All quick tests passed!")
        return 0
    else:
        print(f"\n⚠️ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit(main())
