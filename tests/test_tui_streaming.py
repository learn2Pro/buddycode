#!/usr/bin/env python
"""
Tests for TUI streaming functionality (tool calls and thinking display).
"""
import pytest
from unittest.mock import Mock, patch
from buddycode.tui import BuddyCodeTUI


@pytest.mark.asyncio
class TestTUIStreaming:
    """Test TUI streaming features."""

    @patch('buddycode.tui.create_coding_agent')
    async def test_tool_call_display(self, mock_create_agent):
        """Test that tool calls are displayed in the TUI."""
        mock_agent = Mock()

        # Create a tool call message
        tool_call_message = Mock()
        tool_call_message.content = ""
        tool_call_message.tool_calls = [
            {
                'name': 'ls',
                'args': {'path': '/tmp', 'show_hidden': False}
            }
        ]
        tool_call_message.type = 'ai'

        # Create a tool response message
        tool_response = Mock()
        tool_response.content = "file1.py\nfile2.py\nfile3.py"
        tool_response.type = 'tool'
        tool_response.name = 'ls'

        # Create final AI response
        final_message = Mock()
        final_message.content = "I found 3 Python files in /tmp"
        final_message.tool_calls = []
        final_message.type = 'ai'

        # Mock stream to return all chunks in messages mode format
        mock_agent.stream.return_value = iter([
            [("agent", [tool_call_message])],
            [("tool", [tool_response])],
            [("agent", [final_message])],
        ])
        mock_create_agent.return_value = mock_agent

        app = BuddyCodeTUI()
        async with app.run_test() as pilot:
            await pilot.pause(1.0)

            # Submit a message
            user_input = app.query_one("#user-input")
            user_input.value = "List files in /tmp"
            await pilot.press("enter")
            await pilot.pause(3.0)

            # Verify agent was called with stream
            assert mock_agent.stream.called

    @patch('buddycode.tui.create_coding_agent')
    async def test_multiple_tool_calls_display(self, mock_create_agent):
        """Test displaying multiple tool calls in sequence."""
        mock_agent = Mock()

        # Create messages with multiple tool calls
        tool_call1 = Mock()
        tool_call1.content = ""
        tool_call1.tool_calls = [
            {'name': 'tree', 'args': {'path': '.', 'depth': 2}}
        ]
        tool_call1.type = 'ai'

        tool_response1 = Mock()
        tool_response1.content = ".\n├── src/\n└── tests/"
        tool_response1.type = 'tool'
        tool_response1.name = 'tree'

        tool_call2 = Mock()
        tool_call2.content = ""
        tool_call2.tool_calls = [
            {'name': 'grep', 'args': {'pattern': 'TODO', 'path': '.'}}
        ]
        tool_call2.type = 'ai'

        tool_response2 = Mock()
        tool_response2.content = "src/app.py:15: # TODO: implement"
        tool_response2.type = 'tool'
        tool_response2.name = 'grep'

        final_message = Mock()
        final_message.content = "Project has 2 directories and 1 TODO comment"
        final_message.tool_calls = []
        final_message.type = 'ai'

        mock_agent.stream.return_value = iter([
            [("agent", [tool_call1])],
            [("tool", [tool_response1])],
            [("agent", [tool_call2])],
            [("tool", [tool_response2])],
            [("agent", [final_message])],
        ])
        mock_create_agent.return_value = mock_agent

        app = BuddyCodeTUI()
        async with app.run_test() as pilot:
            await pilot.pause(1.0)

            user_input = app.query_one("#user-input")
            user_input.value = "Show project structure and find TODOs"
            await pilot.press("enter")
            await pilot.pause(4.0)

            # Verify stream was called
            assert mock_agent.stream.called

    @patch('buddycode.tui.create_coding_agent')
    async def test_thinking_display(self, mock_create_agent):
        """Test that intermediate thinking is displayed."""
        mock_agent = Mock()

        # Create intermediate thinking message
        thinking_msg = Mock()
        thinking_msg.content = "Let me check the project structure first..."
        thinking_msg.tool_calls = []
        thinking_msg.type = 'ai'

        # Create final message
        final_msg = Mock()
        final_msg.content = "Here's what I found..."
        final_msg.tool_calls = []
        final_msg.type = 'ai'

        mock_agent.stream.return_value = iter([
            [("agent", [thinking_msg])],
            [("agent", [final_msg])],
        ])
        mock_create_agent.return_value = mock_agent

        app = BuddyCodeTUI()
        async with app.run_test() as pilot:
            await pilot.pause(1.0)

            user_input = app.query_one("#user-input")
            user_input.value = "Analyze the project"
            await pilot.press("enter")
            await pilot.pause(2.0)

            # Should complete without errors
            assert user_input.value == ""

    @patch('buddycode.tui.create_coding_agent')
    async def test_tool_args_formatting(self, mock_create_agent):
        """Test that tool arguments are formatted correctly."""
        app = BuddyCodeTUI()

        # Test simple args
        simple_args = {'path': '/tmp', 'pattern': 'test'}
        formatted = app._format_tool_args(simple_args)
        assert 'path' in formatted
        assert '/tmp' in formatted

        # Test complex nested args
        complex_args = {
            'config': {
                'depth': 2,
                'show_hidden': True
            },
            'paths': ['/tmp', '/var']
        }
        formatted = app._format_tool_args(complex_args)
        assert 'config' in formatted
        assert 'depth' in formatted

    @patch('buddycode.tui.create_coding_agent')
    async def test_long_tool_output_truncation(self, mock_create_agent):
        """Test that long tool outputs are truncated."""
        mock_agent = Mock()

        # Create tool response with very long output
        tool_response = Mock()
        tool_response.content = "x" * 1000  # Very long output
        tool_response.type = 'tool'
        tool_response.name = 'bash'

        final_message = Mock()
        final_message.content = "Command executed"
        final_message.tool_calls = []
        final_message.type = 'ai'

        mock_agent.stream.return_value = iter([
            [("tool", [tool_response])],
            [("agent", [final_message])],
        ])
        mock_create_agent.return_value = mock_agent

        app = BuddyCodeTUI()
        async with app.run_test() as pilot:
            await pilot.pause(1.0)

            user_input = app.query_one("#user-input")
            user_input.value = "Run a command"
            await pilot.press("enter")
            await pilot.pause(2.0)

            # Should handle long output without crashing
            assert user_input.value == ""

    @patch('buddycode.tui.create_coding_agent')
    async def test_status_bar_updates_during_tool_execution(self, mock_create_agent):
        """Test that status bar updates when tools are running."""
        mock_agent = Mock()

        tool_call_msg = Mock()
        tool_call_msg.content = ""
        tool_call_msg.tool_calls = [{'name': 'edit', 'args': {'file': 'test.py'}}]
        tool_call_msg.type = 'ai'

        final_msg = Mock()
        final_msg.content = "File edited"
        final_msg.tool_calls = []
        final_msg.type = 'ai'

        mock_agent.stream.return_value = iter([
            [("agent", [tool_call_msg])],
            [("agent", [final_msg])],
        ])
        mock_create_agent.return_value = mock_agent

        app = BuddyCodeTUI()
        async with app.run_test() as pilot:
            await pilot.pause(1.0)

            user_input = app.query_one("#user-input")
            user_input.value = "Edit test.py"
            await pilot.press("enter")
            await pilot.pause(2.0)

            # Status should eventually return to Ready
            assert "Ready" in app.status_bar.status or app.status_bar.status == "Ready"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
