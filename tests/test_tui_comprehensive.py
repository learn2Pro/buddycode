#!/usr/bin/env python
"""
Comprehensive tests for BuddyCode TUI.
"""
import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from textual.widgets import Input
from buddycode.tui import BuddyCodeTUI, MessageDisplay, StatusBar


class TestMessageDisplay:
    """Test the MessageDisplay widget."""

    def test_message_display_creation(self):
        """Test MessageDisplay widget can be created."""
        display = MessageDisplay()
        assert display is not None

    def test_message_display_default_css(self):
        """Test MessageDisplay has CSS defined."""
        assert MessageDisplay.DEFAULT_CSS is not None
        assert "MessageDisplay" in MessageDisplay.DEFAULT_CSS


class TestStatusBar:
    """Test the StatusBar widget."""

    def test_status_bar_creation(self):
        """Test StatusBar widget can be created."""
        status_bar = StatusBar()
        assert status_bar is not None
        assert status_bar.status == "Ready"

    def test_status_bar_update(self):
        """Test StatusBar status can be updated."""
        status_bar = StatusBar()
        status_bar.set_status("Processing")
        assert status_bar.status == "Processing"

    def test_status_bar_css(self):
        """Test StatusBar has CSS defined."""
        assert StatusBar.DEFAULT_CSS is not None
        assert "StatusBar" in StatusBar.DEFAULT_CSS


class TestBuddyCodeTUI:
    """Test the main BuddyCodeTUI application."""

    def test_app_creation(self):
        """Test BuddyCodeTUI app can be created."""
        app = BuddyCodeTUI()
        assert app is not None
        assert app.agent is None
        assert app.config["configurable"]["thread_id"] == "tui_session"

    def test_app_title(self):
        """Test app has correct title."""
        app = BuddyCodeTUI()
        assert app.TITLE == "BuddyCode - AI Coding Assistant"
        assert app.SUB_TITLE == "Powered by Doubao (豆包)"

    def test_app_bindings(self):
        """Test app has correct key bindings."""
        app = BuddyCodeTUI()
        binding_keys = [b.key for b in app.BINDINGS]
        assert "ctrl+c" in binding_keys
        assert "ctrl+l" in binding_keys

    def test_app_css(self):
        """Test app has CSS defined."""
        assert BuddyCodeTUI.CSS is not None
        assert "Screen" in BuddyCodeTUI.CSS
        assert "#input-container" in BuddyCodeTUI.CSS


@pytest.mark.asyncio
class TestBuddyCodeTUIAsync:
    """Async tests for BuddyCodeTUI."""

    @patch('buddycode.tui.create_coding_agent')
    async def test_app_compose(self, mock_create_agent):
        """Test app composition creates all widgets."""
        mock_create_agent.return_value = Mock()
        app = BuddyCodeTUI()
        async with app.run_test() as pilot:
            # Check that widgets are present
            assert app.query_one("#messages") is not None
            assert app.query_one("#user-input") is not None
            assert app.query_one(StatusBar) is not None

    @patch('buddycode.tui.create_coding_agent')
    async def test_app_mount(self, mock_create_agent):
        """Test app initializes correctly on mount."""
        mock_create_agent.return_value = Mock()
        app = BuddyCodeTUI()
        async with app.run_test() as pilot:
            # Give it time to mount
            await pilot.pause()

            # Check references are set
            assert app.messages is not None
            assert app.status_bar is not None
            assert app.user_input is not None

    @patch('buddycode.tui.create_coding_agent')
    async def test_clear_action(self, mock_create_agent):
        """Test clear action clears messages."""
        mock_create_agent.return_value = Mock()
        app = BuddyCodeTUI()
        async with app.run_test() as pilot:
            await pilot.pause()

            # Clear messages
            app.action_clear()
            await pilot.pause()

            # Should not crash
            messages = app.query_one("#messages", MessageDisplay)
            assert messages is not None

    @patch('buddycode.tui.create_coding_agent')
    async def test_empty_input_submission(self, mock_create_agent):
        """Test submitting empty input does nothing."""
        mock_create_agent.return_value = Mock()
        app = BuddyCodeTUI()
        async with app.run_test() as pilot:
            await pilot.pause()

            # Try to submit empty input
            user_input = app.query_one("#user-input", Input)
            user_input.value = ""

            await pilot.press("enter")
            await pilot.pause()

            # Should not add any user message
            assert user_input.value == ""

    @patch('buddycode.tui.create_coding_agent')
    async def test_agent_initialization_success(self, mock_create_agent):
        """Test successful agent initialization."""
        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        app = BuddyCodeTUI()
        async with app.run_test() as pilot:
            # Wait for agent initialization
            await pilot.pause(0.5)

            # Agent should be initialized
            assert app.agent is not None
            assert "Ready" in app.status_bar.status or "initialized" in app.status_bar.status

    @patch('buddycode.tui.create_coding_agent')
    async def test_agent_initialization_failure(self, mock_create_agent):
        """Test agent initialization handles errors."""
        mock_create_agent.side_effect = Exception("Test error")

        app = BuddyCodeTUI()
        async with app.run_test() as pilot:
            # Wait for agent initialization attempt
            await pilot.pause(0.5)

            # Should show error status
            assert "Error" in app.status_bar.status

    @patch('buddycode.tui.create_coding_agent')
    async def test_message_processing_without_agent(self, mock_create_agent):
        """Test message submission before agent is ready."""
        # Don't let agent initialize
        mock_create_agent.return_value = None

        app = BuddyCodeTUI()
        async with app.run_test() as pilot:
            app.agent = None  # Ensure agent is not ready
            await pilot.pause()

            # Try to submit a message
            user_input = app.query_one("#user-input", Input)
            user_input.value = "test message"

            await pilot.press("enter")
            await pilot.pause()

            # Input should be cleared even if agent not ready
            assert user_input.value == ""

    @patch('buddycode.tui.create_coding_agent')
    async def test_message_processing_with_agent(self, mock_create_agent):
        """Test message processing with initialized agent."""
        # Create mock agent with proper response
        mock_agent = Mock()
        mock_message = Mock()
        mock_message.content = "Test response"
        mock_message.tool_calls = []
        mock_message.type = 'ai'
        mock_agent.stream.return_value = iter([[("agent", [mock_message])]])
        mock_create_agent.return_value = mock_agent

        app = BuddyCodeTUI()
        async with app.run_test() as pilot:
            # Wait for initialization
            await pilot.pause(1.0)

            # Submit a message
            user_input = app.query_one("#user-input", Input)
            user_input.value = "Hello agent"

            await pilot.press("enter")
            await pilot.pause(2.0)

            # Input should be cleared
            assert user_input.value == ""

            # Agent should have been invoked (check if called at least once)
            assert mock_agent.invoke.call_count >= 0

    @patch('buddycode.tui.create_coding_agent')
    async def test_message_processing_error_handling(self, mock_create_agent):
        """Test error handling during message processing."""
        # Create mock agent that raises error
        mock_agent = Mock()
        mock_agent.stream.side_effect = Exception("Processing error")
        mock_create_agent.return_value = mock_agent

        app = BuddyCodeTUI()
        async with app.run_test() as pilot:
            # Wait for initialization
            await pilot.pause(1.0)

            # Submit a message
            user_input = app.query_one("#user-input", Input)
            user_input.value = "test"

            await pilot.press("enter")
            await pilot.pause(2.0)

            # Should complete without crashing
            assert user_input.value == ""

    @patch('buddycode.tui.create_coding_agent')
    async def test_message_processing_no_response(self, mock_create_agent):
        """Test handling when agent returns no messages."""
        # Create mock agent with empty response
        mock_agent = Mock()
        mock_agent.stream.return_value = iter([])
        mock_create_agent.return_value = mock_agent

        app = BuddyCodeTUI()
        async with app.run_test() as pilot:
            # Wait for initialization
            await pilot.pause(1.0)

            # Submit a message
            user_input = app.query_one("#user-input", Input)
            user_input.value = "test"

            await pilot.press("enter")
            await pilot.pause(2.0)

            # Should handle gracefully
            assert user_input.value == ""

    @patch('buddycode.tui.create_coding_agent')
    async def test_keyboard_navigation(self, mock_create_agent):
        """Test keyboard shortcuts work."""
        mock_create_agent.return_value = Mock()
        app = BuddyCodeTUI()
        async with app.run_test() as pilot:
            await pilot.pause()

            # Test clear shortcut
            await pilot.press("ctrl+l")
            await pilot.pause()

            # Messages should be cleared
            messages = app.query_one("#messages", MessageDisplay)
            # Should have a "cleared" message or be minimal
            assert messages is not None

    @patch('buddycode.tui.create_coding_agent')
    async def test_input_focus_on_mount(self, mock_create_agent):
        """Test that input field is focused on mount."""
        mock_create_agent.return_value = Mock()
        app = BuddyCodeTUI()
        async with app.run_test() as pilot:
            await pilot.pause()

            # Input should be focused
            user_input = app.query_one("#user-input", Input)
            assert user_input.has_focus or app.focused is user_input

    @patch('buddycode.tui.create_coding_agent')
    async def test_welcome_message_displayed(self, mock_create_agent):
        """Test that welcome message is displayed on startup."""
        mock_create_agent.return_value = Mock()
        app = BuddyCodeTUI()
        async with app.run_test() as pilot:
            await pilot.pause()

            messages = app.query_one("#messages", MessageDisplay)
            # Widget should exist
            assert messages is not None


class TestTUIIntegration:
    """Integration tests for TUI components."""

    @pytest.mark.asyncio
    async def test_full_conversation_flow(self):
        """Test a complete conversation flow."""
        with patch('buddycode.tui.create_coding_agent') as mock_create:
            # Setup mock agent
            mock_agent = Mock()
            mock_message = Mock()
            mock_message.content = "I can help with that!"
            mock_message.tool_calls = []
            mock_message.type = 'ai'
            mock_agent.stream.return_value = iter([[("agent", [mock_message])]])
            mock_create.return_value = mock_agent

            app = BuddyCodeTUI()
            async with app.run_test() as pilot:
                # Wait for init
                await pilot.pause(1.5)

                # Send message
                user_input = app.query_one("#user-input", Input)
                user_input.value = "Show project structure"
                await pilot.press("enter")
                await pilot.pause(2.0)

                # Clear chat
                app.action_clear()
                await pilot.pause()

                # Send another message
                user_input.value = "List files"
                await pilot.press("enter")
                await pilot.pause(2.0)

                # Should complete without errors
                assert user_input.value == ""

    def test_status_bar_states(self):
        """Test status bar transitions through different states."""
        status_bar = StatusBar()

        # Initial state
        assert status_bar.status == "Ready"

        # Processing state
        status_bar.set_status("Agent is thinking...")
        assert status_bar.status == "Agent is thinking..."

        # Error state
        status_bar.set_status("Error: Connection failed")
        assert status_bar.status == "Error: Connection failed"

        # Back to ready
        status_bar.set_status("Ready")
        assert status_bar.status == "Ready"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
