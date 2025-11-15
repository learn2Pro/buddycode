"""
BuddyCode TUI - Textual-based Terminal User Interface for Code Agent

A beautiful terminal interface for interacting with the BuddyCode agent.
"""
from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Header, Footer, Input, RichLog, Static
from textual.binding import Binding
from textual import work
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
import asyncio
from buddycode.react_agent import create_coding_agent


class MessageDisplay(RichLog):
    """Widget for displaying chat messages."""

    DEFAULT_CSS = """
    MessageDisplay {
        border: solid $primary;
        height: 1fr;
        background: $surface;
    }
    """

    def on_mount(self) -> None:
        """Set up the message display on mount."""
        self.can_focus = False


class StatusBar(Static):
    """Status bar showing agent state."""

    DEFAULT_CSS = """
    StatusBar {
        dock: bottom;
        height: 1;
        background: $primary;
        color: $text;
        padding: 0 1;
    }
    """

    def __init__(self) -> None:
        super().__init__()
        self.status = "Ready"

    def on_mount(self) -> None:
        """Update display on mount."""
        self.update(f"[bold]Status:[/bold] {self.status}")

    def set_status(self, status: str) -> None:
        """Update the status message."""
        self.status = status
        self.update(f"[bold]Status:[/bold] {self.status}")


class BuddyCodeTUI(App):
    """Main Textual application for BuddyCode."""

    CSS = """
    Screen {
        background: $surface;
    }

    #input-container {
        dock: bottom;
        height: 3;
        background: $panel;
        padding: 0 1;
    }

    Input {
        width: 1fr;
    }

    #main-container {
        height: 1fr;
        padding: 1;
    }
    """

    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit", show=True),
        Binding("ctrl+l", "clear", "Clear", show=True),
    ]

    TITLE = "BuddyCode - AI Coding Assistant"
    SUB_TITLE = "Powered by Doubao (豆包)"

    def __init__(self):
        super().__init__()
        self.agent = None
        self.config = {"configurable": {"thread_id": "tui_session"}}

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Header()

        with Container(id="main-container"):
            yield MessageDisplay(id="messages")

        with Vertical(id="input-container"):
            yield Input(placeholder="Type your message... (Press Enter to send)", id="user-input")

        yield StatusBar()
        yield Footer()

    def on_mount(self) -> None:
        """Initialize the app on mount."""
        self.messages = self.query_one("#messages", MessageDisplay)
        self.status_bar = self.query_one(StatusBar)
        self.user_input = self.query_one("#user-input", Input)

        # Show welcome message
        self.messages.write(Panel(
            Markdown("""# Welcome to BuddyCode! 🤖

An AI-powered coding assistant with file system tools.

**Available Tools:**
- 📁 `ls` - List files and directories
- 🔍 `grep` - Search in files
- 🌲 `tree` - Show directory structure
- 💻 `bash` - Execute commands
- ✏️  `edit` - Edit files
- 📝 `todo_write` - Manage tasks

**Quick Examples:**
- "Show me the project structure"
- "Find all TODO comments in Python files"
- "Create a Button component in /tmp"
- "Help me fix the bug in react_agent.py"

Type your message below and press Enter to start!
"""),
            title="[bold cyan]BuddyCode v0.1.0[/bold cyan]",
            border_style="cyan"
        ))

        # Initialize agent in background
        self.init_agent()

        # Focus the input
        self.user_input.focus()

    @work(exclusive=True)
    async def init_agent(self) -> None:
        """Initialize the agent asynchronously."""
        self.status_bar.set_status("Initializing agent...")

        try:
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            self.agent = await loop.run_in_executor(None, create_coding_agent)
            self.status_bar.set_status("Ready - Agent initialized ✓")
        except Exception as e:
            self.status_bar.set_status(f"Error: {e}")
            self.messages.write(Panel(
                f"[bold red]Failed to initialize agent:[/bold red]\n{e}",
                border_style="red"
            ))

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle user input submission."""
        user_message = event.value.strip()

        if not user_message:
            return

        # Clear input
        self.user_input.value = ""

        # Display user message
        self.messages.write(Panel(
            Text(user_message, style="bold cyan"),
            title="[bold]You[/bold]",
            border_style="cyan"
        ))

        # Check if agent is ready
        if self.agent is None:
            self.messages.write(Panel(
                "[yellow]Agent is still initializing... Please wait.[/yellow]",
                border_style="yellow"
            ))
            return

        # Process with agent (don't await - @work decorator handles async)
        self.process_message(user_message)

    @work(exclusive=True)
    async def process_message(self, message: str) -> None:
        """Process message with the agent."""
        self.status_bar.set_status("Agent is thinking...")

        try:
            # Create a placeholder for streaming output
            thinking_panel = self.messages.write(Panel(
                "[dim]Agent is processing...[/dim]",
                title="[bold green]🤖 Agent[/bold green]",
                border_style="green"
            ))

            # Run agent in thread pool
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: self.agent.invoke(
                    {"messages": [("user", message)]},
                    self.config
                )
            )

            # Clear the placeholder (Textual doesn't support editing, so we add new)
            # Extract final response
            if "messages" in result and len(result["messages"]) > 0:
                last_message = result["messages"][-1]
                response = last_message.content if hasattr(last_message, 'content') else str(last_message)

                # Display agent response with markdown
                self.messages.write(Panel(
                    Markdown(response),
                    title="[bold green]🤖 Agent[/bold green]",
                    border_style="green"
                ))
            else:
                self.messages.write(Panel(
                    "[yellow]No response from agent[/yellow]",
                    border_style="yellow"
                ))

            self.status_bar.set_status("Ready")

        except Exception as e:
            self.messages.write(Panel(
                f"[bold red]Error:[/bold red]\n{str(e)}",
                border_style="red"
            ))
            self.status_bar.set_status("Error occurred")

        finally:
            # Scroll to bottom
            self.messages.scroll_end()

    def action_clear(self) -> None:
        """Clear the message display."""
        self.messages.clear()
        self.messages.write(Panel(
            "[dim]Chat cleared[/dim]",
            border_style="blue"
        ))


def main():
    """Entry point for the TUI application."""
    app = BuddyCodeTUI()
    app.run()


if __name__ == "__main__":
    main()
