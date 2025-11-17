#!/usr/bin/env python
"""
Tests for TUI copy functionality.
"""
import pytest
from unittest.mock import Mock, patch
from buddycode.tui import BuddyCodeTUI


@pytest.mark.asyncio
class TestTUICopy:
    """Test TUI clipboard copy features."""

    @patch('buddycode.tui.create_coding_agent')
    @patch('buddycode.tui.pyperclip')
    async def test_copy_last_response(self, mock_pyperclip, mock_create_agent):
        """Test copying last agent response to clipboard."""
        mock_agent = Mock()

        # Create a response message
        mock_message = Mock()
        mock_message.content = "Test response for copying"
        mock_message.tool_calls = []
        mock_message.type = 'ai'

        mock_agent.stream.return_value = iter([
            [("agent", [mock_message])]
        ])
        mock_create_agent.return_value = mock_agent

        app = BuddyCodeTUI()
        async with app.run_test() as pilot:
            await pilot.pause(1.0)

            # Submit a message to get a response
            user_input = app.query_one("#user-input")
            user_input.value = "Test message"
            await pilot.press("enter")
            await pilot.pause(2.0)

            # Set last_response manually for testing
            app.last_response = "Test response for copying"

            # Trigger copy action
            app.action_copy_last()

            # Verify pyperclip.copy was called with correct content
            mock_pyperclip.copy.assert_called_once_with("Test response for copying")

    @patch('buddycode.tui.create_coding_agent')
    @patch('buddycode.tui.pyperclip')
    async def test_copy_with_no_response(self, mock_pyperclip, mock_create_agent):
        """Test copying when there is no response available."""
        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        app = BuddyCodeTUI()
        async with app.run_test() as pilot:
            await pilot.pause(1.0)

            # Trigger copy action without any response
            app.action_copy_last()

            # Verify pyperclip.copy was NOT called
            mock_pyperclip.copy.assert_not_called()

    @patch('buddycode.tui.create_coding_agent')
    @patch('buddycode.tui.pyperclip')
    async def test_copy_failure_handling(self, mock_pyperclip, mock_create_agent):
        """Test handling of copy failures."""
        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        # Mock pyperclip.copy to raise an exception
        mock_pyperclip.copy.side_effect = Exception("Clipboard unavailable")

        app = BuddyCodeTUI()
        async with app.run_test() as pilot:
            await pilot.pause(1.0)

            # Set a response
            app.last_response = "Test response"

            # Trigger copy action
            app.action_copy_last()

            # Should handle the error gracefully
            # (No assertion needed - just verify it doesn't crash)

    @patch('buddycode.tui.create_coding_agent')
    @patch('buddycode.tui.pyperclip')
    async def test_copy_long_response(self, mock_pyperclip, mock_create_agent):
        """Test copying a long response."""
        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        app = BuddyCodeTUI()
        async with app.run_test() as pilot:
            await pilot.pause(1.0)

            # Set a long response
            long_response = "x" * 5000
            app.last_response = long_response

            # Trigger copy action
            app.action_copy_last()

            # Verify the full response was copied
            mock_pyperclip.copy.assert_called_once_with(long_response)

    @patch('buddycode.tui.create_coding_agent')
    @patch('buddycode.tui.pyperclip')
    async def test_copy_with_special_characters(self, mock_pyperclip, mock_create_agent):
        """Test copying response with special characters."""
        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        app = BuddyCodeTUI()
        async with app.run_test() as pilot:
            await pilot.pause(1.0)

            # Set response with special characters
            special_response = "Test with\nnewlines\tand\ttabs 🎨 emojis"
            app.last_response = special_response

            # Trigger copy action
            app.action_copy_last()

            # Verify special characters are preserved
            mock_pyperclip.copy.assert_called_once_with(special_response)

    @patch('buddycode.tui.create_coding_agent')
    @patch('buddycode.tui.pyperclip')
    async def test_copy_updates_status_bar(self, mock_pyperclip, mock_create_agent):
        """Test that copy action updates the status bar."""
        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        app = BuddyCodeTUI()
        async with app.run_test() as pilot:
            await pilot.pause(1.0)

            # Set a response
            app.last_response = "Test response"

            # Trigger copy action
            app.action_copy_last()

            # Verify status bar was updated
            assert "Copied" in app.status_bar.status or "clipboard" in app.status_bar.status.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
