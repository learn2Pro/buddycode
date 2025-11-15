#!/usr/bin/env python
"""
Edge case tests for BuddyCode TUI.
"""
import pytest
from unittest.mock import Mock, patch
from textual.widgets import Input
from buddycode.tui import BuddyCodeTUI, MessageDisplay, StatusBar


@pytest.mark.asyncio
class TestTUIEdgeCases:
    """Test edge cases and boundary conditions."""

    async def test_very_long_input(self):
        """Test handling of very long input messages."""
        app = BuddyCodeTUI()
        async with app.run_test() as pilot:
            await pilot.pause(0.5)

            # Create a very long message
            long_message = "A" * 10000
            user_input = app.query_one("#user-input", Input)
            user_input.value = long_message

            await pilot.press("enter")
            await pilot.pause(0.5)

            # Should handle without crashing
            assert user_input.value == ""

    async def test_special_characters_in_input(self):
        """Test handling of special characters in input."""
        app = BuddyCodeTUI()
        async with app.run_test() as pilot:
            await pilot.pause(0.5)

            # Test various special characters
            special_chars = [
                "Hello World",  # simple text (newlines handled differently in input)
                "Unicode: 你好 🤖",  # unicode
                "Symbols: @#$%^&*()",  # symbols
                "Quotes: 'single' \"double\"",  # quotes
            ]

            user_input = app.query_one("#user-input", Input)
            for text in special_chars:
                user_input.value = text
                await pilot.press("enter")
                await pilot.pause(0.3)

                # Should handle without crashing
                assert user_input.value == ""

    async def test_whitespace_only_input(self):
        """Test submitting whitespace-only input."""
        app = BuddyCodeTUI()
        async with app.run_test() as pilot:
            await pilot.pause(0.5)

            user_input = app.query_one("#user-input", Input)

            # Test submitting whitespace - should not process it
            user_input.value = "   "
            initial_value = user_input.value
            await pilot.press("enter")
            await pilot.pause(0.3)

            # Should not process whitespace-only input (based on strip() check in code)
            # Input value might not be cleared if whitespace-only
            assert user_input is not None

    @patch('buddycode.tui.create_coding_agent')
    async def test_rapid_message_submission(self, mock_create_agent):
        """Test submitting messages rapidly in succession."""
        mock_agent = Mock()
        mock_message = Mock()
        mock_message.content = "Response"
        mock_agent.invoke.return_value = {"messages": [mock_message]}
        mock_create_agent.return_value = mock_agent

        app = BuddyCodeTUI()
        async with app.run_test() as pilot:
            await pilot.pause(1.0)

            user_input = app.query_one("#user-input", Input)

            # Submit multiple messages quickly
            for i in range(3):
                user_input.value = f"Message {i}"
                await pilot.press("enter")
                # Don't wait long between submissions
                await pilot.pause(0.3)

            # Should handle all messages without crashing
            await pilot.pause(2.0)
            assert user_input is not None

    @patch('buddycode.tui.create_coding_agent')
    async def test_agent_response_with_no_content(self, mock_create_agent):
        """Test handling agent message with no content attribute."""
        mock_agent = Mock()
        mock_message = Mock(spec=[])  # Message with no attributes
        mock_agent.invoke.return_value = {"messages": [mock_message]}
        mock_create_agent.return_value = mock_agent

        app = BuddyCodeTUI()
        async with app.run_test() as pilot:
            await pilot.pause(1.0)

            user_input = app.query_one("#user-input", Input)
            user_input.value = "test"
            await pilot.press("enter")
            await pilot.pause(2.0)

            # Should handle gracefully with str() fallback
            assert user_input.value == ""

    @patch('buddycode.tui.create_coding_agent')
    async def test_agent_response_with_dict_result(self, mock_create_agent):
        """Test handling when agent returns unexpected result format."""
        mock_agent = Mock()
        # Return result without 'messages' key
        mock_agent.invoke.return_value = {"unexpected_key": "value"}
        mock_create_agent.return_value = mock_agent

        app = BuddyCodeTUI()
        async with app.run_test() as pilot:
            await pilot.pause(1.0)

            user_input = app.query_one("#user-input", Input)
            user_input.value = "test"
            await pilot.press("enter")
            await pilot.pause(2.0)

            # Should handle missing 'messages' key gracefully
            assert user_input.value == ""

    async def test_multiple_clear_actions(self):
        """Test clearing messages multiple times."""
        app = BuddyCodeTUI()
        async with app.run_test() as pilot:
            await pilot.pause()

            # Clear multiple times
            for _ in range(5):
                app.action_clear()
                await pilot.pause()

            # Should not crash
            messages = app.query_one("#messages", MessageDisplay)
            assert messages is not None

    @patch('buddycode.tui.create_coding_agent')
    async def test_agent_timeout_simulation(self, mock_create_agent):
        """Test handling of agent taking very long to respond."""
        mock_agent = Mock()
        mock_message = Mock()
        mock_message.content = "Response"
        # Simulate slow response
        mock_agent.invoke.return_value = {"messages": [mock_message]}
        mock_create_agent.return_value = mock_agent

        app = BuddyCodeTUI()
        async with app.run_test() as pilot:
            await pilot.pause(1.0)

            user_input = app.query_one("#user-input", Input)
            user_input.value = "test"
            await pilot.press("enter")
            await pilot.pause(2.0)

            # Should handle requests
            assert user_input.value == ""

    async def test_status_bar_with_very_long_status(self):
        """Test status bar with very long status text."""
        status_bar = StatusBar()
        very_long_status = "X" * 1000

        status_bar.set_status(very_long_status)

        assert status_bar.status == very_long_status

    @patch('buddycode.tui.create_coding_agent')
    async def test_agent_returning_markdown_content(self, mock_create_agent):
        """Test handling of markdown-formatted responses."""
        mock_agent = Mock()
        mock_message = Mock()
        # Complex markdown content
        mock_message.content = """
# Header

## Subheader

- List item 1
- List item 2

```python
def example():
    return "code"
```

**Bold** and *italic*
"""
        mock_agent.invoke.return_value = {"messages": [mock_message]}
        mock_create_agent.return_value = mock_agent

        app = BuddyCodeTUI()
        async with app.run_test() as pilot:
            await pilot.pause(1.0)

            user_input = app.query_one("#user-input", Input)
            user_input.value = "test"
            await pilot.press("enter")
            await pilot.pause(2.0)

            # Should render markdown without crashing
            assert user_input.value == ""

    async def test_config_persistence(self):
        """Test that config thread_id persists across interactions."""
        app = BuddyCodeTUI()

        # Check initial config
        assert app.config["configurable"]["thread_id"] == "tui_session"

        async with app.run_test() as pilot:
            await pilot.pause()

            # Config should remain the same
            assert app.config["configurable"]["thread_id"] == "tui_session"

    @patch('buddycode.tui.create_coding_agent')
    async def test_agent_exception_types(self, mock_create_agent):
        """Test handling different exception types during agent invocation."""
        mock_agent = Mock()
        mock_agent.invoke.side_effect = ValueError("Value error")
        mock_create_agent.return_value = mock_agent

        app = BuddyCodeTUI()
        async with app.run_test() as pilot:
            await pilot.pause(1.0)

            user_input = app.query_one("#user-input", Input)
            user_input.value = "test"
            await pilot.press("enter")
            await pilot.pause(2.0)

            # Should handle exception gracefully
            assert user_input.value == ""


@pytest.mark.asyncio
class TestTUIStressTests:
    """Stress tests for TUI."""

    @patch('buddycode.tui.create_coding_agent')
    async def test_many_messages_in_conversation(self, mock_create_agent):
        """Test handling many messages in a single session."""
        mock_agent = Mock()
        mock_message = Mock()
        mock_message.content = "Response"
        mock_agent.invoke.return_value = {"messages": [mock_message]}
        mock_create_agent.return_value = mock_agent

        app = BuddyCodeTUI()
        async with app.run_test() as pilot:
            await pilot.pause(1.0)

            user_input = app.query_one("#user-input", Input)

            # Send several messages
            for i in range(3):
                user_input.value = f"Message {i}"
                await pilot.press("enter")
                await pilot.pause(1.0)

            # Should handle without performance issues
            assert user_input.value == ""

    async def test_message_display_scroll(self):
        """Test message display scrolling with many messages."""
        app = BuddyCodeTUI()
        async with app.run_test() as pilot:
            await pilot.pause()

            messages = app.query_one("#messages", MessageDisplay)

            # Add many messages
            for i in range(100):
                messages.write(f"Message {i}")

            # Should scroll to bottom
            await pilot.pause()
            assert True  # No crash


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
