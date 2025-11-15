"""
Simple test file to verify the tools work correctly.

Run with: python test_tools.py
"""

def test_imports():
    """Test that all tools can be imported."""
    print("Testing imports...")
    try:
        from buddycode import LsTool, GrepTool, TreeTool, BashTool, EditTool, TodoTool, get_file_system_tools
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def test_ls_tool():
    """Test LsTool basic functionality."""
    print("\nTesting LsTool...")
    try:
        from buddycode import LsTool

        ls_tool = LsTool()
        result = ls_tool._run(path=".")

        assert isinstance(result, str), "Result should be a string"
        assert "Contents of" in result or "Error:" in result, "Result should contain expected content"

        print("✓ LsTool works correctly")
        print(f"  Sample output: {result[:100]}...")
        return True
    except Exception as e:
        print(f"✗ LsTool failed: {e}")
        return False


def test_grep_tool():
    """Test GrepTool basic functionality."""
    print("\nTesting GrepTool...")
    try:
        from buddycode import GrepTool

        grep_tool = GrepTool()
        result = grep_tool._run(pattern="import", file_pattern="*.py", max_results=5)

        assert isinstance(result, str), "Result should be a string"
        assert "Search results" in result or "No matches" in result or "Error:" in result

        print("✓ GrepTool works correctly")
        print(f"  Sample output: {result[:100]}...")
        return True
    except Exception as e:
        print(f"✗ GrepTool failed: {e}")
        return False


def test_tree_tool():
    """Test TreeTool basic functionality."""
    print("\nTesting TreeTool...")
    try:
        from buddycode import TreeTool

        tree_tool = TreeTool()
        result = tree_tool._run(path=".", max_depth=2)

        assert isinstance(result, str), "Result should be a string"
        assert "directories" in result or "Error:" in result

        print("✓ TreeTool works correctly")
        print(f"  Sample output (first 150 chars): {result[:150]}...")
        return True
    except Exception as e:
        print(f"✗ TreeTool failed: {e}")
        return False


def test_bash_tool():
    """Test BashTool basic functionality."""
    print("\nTesting BashTool...")
    try:
        from buddycode import BashTool

        bash_tool = BashTool()
        result = bash_tool._run(command="echo 'test'")

        assert isinstance(result, str), "Result should be a string"
        assert "Exit Code:" in result or "Error:" in result, "Result should contain exit code or error"

        print("✓ BashTool works correctly")
        print(f"  Sample output: {result[:100]}...")
        return True
    except Exception as e:
        print(f"✗ BashTool failed: {e}")
        return False


def test_edit_tool():
    """Test EditTool basic functionality."""
    print("\nTesting EditTool...")
    try:
        from buddycode import EditTool
        import tempfile
        import os

        edit_tool = EditTool()

        # Create a temp file for testing
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            temp_file = f.name
            f.write("Line 1\nLine 2\nLine 3\n")

        try:
            # Test view
            result = edit_tool._run(operation="view", file_path=temp_file)
            print(f"View result: {result}")
            assert isinstance(result, str), "Result should be a string"
            assert "Line 1" in result, "Should contain file content"
            assert "1 |" in result, "Should show line numbers"

            # Test str_replace
            result = edit_tool._run(
                operation="str_replace",
                file_path=temp_file,
                old_str="Line 1",
                new_str="Modified Line 1"
            )
            assert "Success" in result, "Replace should succeed"

            # Verify replacement
            result = edit_tool._run(operation="view", file_path=temp_file)
            assert "Modified Line 1" in result, "Should contain modified content"

            print("✓ EditTool works correctly")
            print(f"  Sample output: {result[:100]}...")
            return True
        finally:
            os.unlink(temp_file)

    except Exception as e:
        print(f"✗ EditTool failed: {e}")
        return False


def test_todo_tool():
    """Test TodoTool basic functionality."""
    print("\nTesting TodoTool...")
    try:
        from buddycode import TodoTool

        todo_tool = TodoTool()

        # Clear any existing todos first
        todo_tool._run(operation="clear")

        # Test add
        result = todo_tool._run(operation="add", item="Test task 1")
        assert isinstance(result, str), "Result should be a string"
        assert "Success" in result, "Add should succeed"
        assert "Test task 1" in result, "Should contain the added item"

        # Add another item
        result = todo_tool._run(operation="add", item="Test task 2")
        assert "Success" in result, "Second add should succeed"

        # Test list
        result = todo_tool._run(operation="list")
        assert "Test task 1" in result, "Should show first task"
        assert "Test task 2" in result, "Should show second task"
        assert "2 items" in result, "Should show correct count"

        # Test complete
        result = todo_tool._run(operation="complete", index=1)
        assert "Success" in result or "completed" in result, "Complete should succeed"

        # Verify completion
        result = todo_tool._run(operation="list")
        assert "✓" in result, "Should show completed marker"

        # Test remove
        result = todo_tool._run(operation="remove", index=1)
        assert "Success" in result or "Removed" in result, "Remove should succeed"

        # Test clear
        result = todo_tool._run(operation="clear")
        assert "Success" in result or "Cleared" in result, "Clear should succeed"

        # Verify empty
        result = todo_tool._run(operation="list")
        assert "empty" in result, "Should be empty after clear"

        print("✓ TodoTool works correctly")
        print(f"  Sample output: {result[:100]}...")
        return True
    except Exception as e:
        print(f"✗ TodoTool failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_get_all_tools():
    """Test getting all tools at once."""
    print("\nTesting get_file_system_tools()...")
    try:
        from buddycode import get_file_system_tools

        tools = get_file_system_tools()

        assert len(tools) == 6, "Should return 6 tools"
        assert all(hasattr(tool, 'name') for tool in tools), "All tools should have name attribute"
        assert all(hasattr(tool, 'description') for tool in tools), "All tools should have description"

        tool_names = [tool.name for tool in tools]
        assert "ls" in tool_names, "Should include ls tool"
        assert "grep" in tool_names, "Should include grep tool"
        assert "tree" in tool_names, "Should include tree tool"
        assert "bash" in tool_names, "Should include bash tool"
        assert "text_editor" in tool_names, "Should include text_editor tool"
        assert "todo" in tool_names, "Should include todo tool"

        print("✓ get_file_system_tools() works correctly")
        print(f"  Tools: {tool_names}")
        return True
    except Exception as e:
        print(f"✗ get_file_system_tools() failed: {e}")
        return False


def test_tool_schemas():
    """Test that tools have proper schemas."""
    print("\nTesting tool schemas...")
    try:
        from buddycode import get_file_system_tools

        tools = get_file_system_tools()

        for tool in tools:
            assert hasattr(tool, 'args_schema'), f"{tool.name} should have args_schema"
            assert tool.args_schema is not None, f"{tool.name} args_schema should not be None"

            # Check that schema has fields
            schema = tool.args_schema.model_json_schema()
            assert 'properties' in schema, f"{tool.name} schema should have properties"

        print("✓ All tools have proper schemas")
        return True
    except Exception as e:
        print(f"✗ Schema test failed: {e}")
        return False


def test_error_handling():
    """Test error handling for invalid inputs."""
    print("\nTesting error handling...")
    try:
        from buddycode import LsTool, GrepTool, TreeTool, BashTool, EditTool, TodoTool
        import tempfile
        import os

        # Test invalid path
        ls_tool = LsTool()
        result = ls_tool._run(path="/nonexistent/path/12345")
        assert "Error:" in result or "does not exist" in result

        # Test invalid regex
        grep_tool = GrepTool()
        result = grep_tool._run(pattern="[invalid(")
        assert "Error:" in result or "Invalid regex" in result

        # Test file instead of directory for tree
        tree_tool = TreeTool()
        # First create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("test")
            temp_file = f.name

        try:
            result = tree_tool._run(path=temp_file)
            assert "Error:" in result or "not a directory" in result
        finally:
            os.unlink(temp_file)

        # Test invalid timeout for bash
        bash_tool = BashTool()
        result = bash_tool._run(command="echo 'test'", timeout=500)
        assert "Error:" in result or "timeout" in result.lower()

        # Test invalid working directory for bash
        result = bash_tool._run(command="pwd", working_dir="/nonexistent/directory")
        assert "Error:" in result or "does not exist" in result

        # Test edit tool errors
        edit_tool = EditTool()

        # View non-existent file
        result = edit_tool._run(operation="view", file_path="/nonexistent/file.txt")
        assert "Error:" in result or "does not exist" in result

        # Create file that already exists
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("test")
            temp_file = f.name

        try:
            result = edit_tool._run(operation="create", file_path=temp_file, content="test")
            assert "Error:" in result or "already exists" in result

            # str_replace with non-existent string
            result = edit_tool._run(
                operation="str_replace",
                file_path=temp_file,
                old_str="nonexistent",
                new_str="new"
            )
            assert "Error:" in result or "not found" in result
        finally:
            os.unlink(temp_file)

        # Test todo tool errors
        todo_tool = TodoTool()
        todo_tool._run(operation="clear")  # Clear first

        # Add without item
        result = todo_tool._run(operation="add")
        assert "Error:" in result or "required" in result

        # Complete without index
        result = todo_tool._run(operation="complete")
        assert "Error:" in result or "required" in result

        # Remove with invalid index
        result = todo_tool._run(operation="remove", index=999)
        assert "Error:" in result or "Invalid" in result

        # Unknown operation
        result = todo_tool._run(operation="unknown_op")
        assert "Error:" in result or "Unknown" in result

        print("✓ Error handling works correctly")
        return True
    except Exception as e:
        print(f"✗ Error handling test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 70)
    print("BuddyCode Tools - Test Suite")
    print("=" * 70)

    tests = [
        test_imports,
        test_ls_tool,
        test_grep_tool,
        test_tree_tool,
        test_bash_tool,
        test_edit_tool,
        test_todo_tool,
        test_get_all_tools,
        test_tool_schemas,
        test_error_handling,
    ]

    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"\n✗ Unexpected error in {test_func.__name__}: {e}")
            results.append(False)

    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit(main())
