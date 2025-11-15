#!/usr/bin/env python
"""
Widget-specific tests for BuddyCode TUI components.
"""
import pytest
from buddycode.tui import MessageDisplay, StatusBar
from textual.widgets import RichLog, Static


class TestMessageDisplayWidget:
    """Detailed tests for MessageDisplay widget."""

    def test_inherits_from_richlog(self):
        """Test MessageDisplay inherits from RichLog."""
        display = MessageDisplay()
        assert isinstance(display, RichLog)

    def test_default_properties(self):
        """Test default properties of MessageDisplay."""
        display = MessageDisplay()
        assert hasattr(display, 'DEFAULT_CSS')
        assert 'border' in display.DEFAULT_CSS
        assert 'height' in display.DEFAULT_CSS
        assert 'background' in display.DEFAULT_CSS

    def test_css_specificity(self):
        """Test CSS contains required selectors."""
        css = MessageDisplay.DEFAULT_CSS
        assert 'MessageDisplay {' in css
        assert 'border:' in css
        assert '$primary' in css or '$surface' in css

    @pytest.mark.asyncio
    async def test_write_message(self):
        """Test writing messages to display."""
        from textual.app import App

        class TestApp(App):
            def compose(self):
                yield MessageDisplay(id="test-display")

        app = TestApp()
        async with app.run_test() as pilot:
            display = app.query_one("#test-display", MessageDisplay)

            # Write a message
            display.write("Test message")
            await pilot.pause()

            # Should not crash
            assert display is not None

    @pytest.mark.asyncio
    async def test_multiple_writes(self):
        """Test writing multiple messages."""
        from textual.app import App

        class TestApp(App):
            def compose(self):
                yield MessageDisplay(id="test-display")

        app = TestApp()
        async with app.run_test() as pilot:
            display = app.query_one("#test-display", MessageDisplay)

            # Write multiple messages
            for i in range(10):
                display.write(f"Message {i}")

            await pilot.pause()

            # Should not crash
            assert display is not None

    @pytest.mark.asyncio
    async def test_clear_messages(self):
        """Test clearing messages from display."""
        from textual.app import App

        class TestApp(App):
            def compose(self):
                yield MessageDisplay(id="test-display")

        app = TestApp()
        async with app.run_test() as pilot:
            display = app.query_one("#test-display", MessageDisplay)

            # Write and clear
            display.write("Test message")
            await pilot.pause()

            display.clear()
            await pilot.pause()

            # Should not crash
            assert display is not None


class TestStatusBarWidget:
    """Detailed tests for StatusBar widget."""

    def test_inherits_from_static(self):
        """Test StatusBar inherits from Static."""
        status_bar = StatusBar()
        assert isinstance(status_bar, Static)

    def test_initial_status(self):
        """Test initial status is 'Ready'."""
        status_bar = StatusBar()
        assert status_bar.status == "Ready"

    def test_css_docking(self):
        """Test StatusBar CSS includes dock bottom."""
        css = StatusBar.DEFAULT_CSS
        assert 'StatusBar {' in css
        assert 'dock: bottom' in css
        assert 'height: 1' in css

    def test_css_styling(self):
        """Test StatusBar has proper styling."""
        css = StatusBar.DEFAULT_CSS
        assert 'background:' in css
        assert 'color:' in css
        assert 'padding:' in css

    def test_status_update_changes_internal_state(self):
        """Test set_status updates internal status."""
        status_bar = StatusBar()
        original_status = status_bar.status

        status_bar.set_status("New status")

        assert status_bar.status != original_status
        assert status_bar.status == "New status"

    def test_status_with_markup(self):
        """Test status with Rich markup."""
        status_bar = StatusBar()
        status_bar.set_status("[bold red]Error![/bold red]")

        assert "[bold red]Error![/bold red]" in status_bar.status

    def test_status_with_emoji(self):
        """Test status with emoji characters."""
        status_bar = StatusBar()
        status_bar.set_status("Ready ✓ 🤖")

        assert "✓" in status_bar.status
        assert "🤖" in status_bar.status

    def test_empty_status(self):
        """Test setting empty status."""
        status_bar = StatusBar()
        status_bar.set_status("")

        assert status_bar.status == ""

    def test_very_long_status(self):
        """Test status bar with very long text."""
        status_bar = StatusBar()
        long_text = "X" * 500

        status_bar.set_status(long_text)

        assert status_bar.status == long_text

    def test_status_with_newlines(self):
        """Test status with newline characters."""
        status_bar = StatusBar()
        status_bar.set_status("Line 1\nLine 2")

        assert "\n" in status_bar.status

    def test_multiple_status_updates(self):
        """Test updating status multiple times."""
        status_bar = StatusBar()
        statuses = ["Status 1", "Status 2", "Status 3", "Status 4"]

        for status in statuses:
            status_bar.set_status(status)
            assert status_bar.status == status

    @pytest.mark.asyncio
    async def test_status_bar_in_app(self):
        """Test StatusBar widget in a Textual app."""
        from textual.app import App

        class TestApp(App):
            def compose(self):
                yield StatusBar()

        app = TestApp()
        async with app.run_test() as pilot:
            status_bar = app.query_one(StatusBar)

            # Test initial state
            assert status_bar.status == "Ready"

            # Test update
            status_bar.set_status("Processing...")
            await pilot.pause()

            assert status_bar.status == "Processing..."


class TestWidgetIntegration:
    """Test how widgets work together."""

    @pytest.mark.asyncio
    async def test_message_display_and_status_bar_together(self):
        """Test MessageDisplay and StatusBar in same app."""
        from textual.app import App

        class TestApp(App):
            def compose(self):
                yield MessageDisplay(id="messages")
                yield StatusBar()

        app = TestApp()
        async with app.run_test() as pilot:
            messages = app.query_one("#messages", MessageDisplay)
            status_bar = app.query_one(StatusBar)

            # Both widgets should be present
            assert messages is not None
            assert status_bar is not None

            # Test interaction
            messages.write("User message")
            status_bar.set_status("Processing")
            await pilot.pause()

            assert messages is not None
            assert status_bar.status == "Processing"

    @pytest.mark.asyncio
    async def test_widget_styling_in_app(self):
        """Test that widgets have proper styling when in app."""
        from textual.app import App

        class TestApp(App):
            CSS = """
            MessageDisplay {
                border: solid green;
            }
            StatusBar {
                background: blue;
            }
            """

            def compose(self):
                yield MessageDisplay(id="messages")
                yield StatusBar()

        app = TestApp()
        async with app.run_test() as pilot:
            # Should compose without errors
            await pilot.pause()
            assert True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
