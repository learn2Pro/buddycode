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

    def _format_tool_args(self, args: dict) -> str:
        """Format tool arguments for display."""
        import json
        try:
            return json.dumps(args, indent=2, ensure_ascii=False)
        except Exception:
            return str(args)

    async def _stream_agent_response(self, message: str):
        """Generator that yields streaming chunks from the agent."""
        loop = asyncio.get_event_loop()

        # Create a generator that streams chunks
        def stream_gen():
            for chunk in self.agent.stream(
                {"messages": [("user", message)]},
                self.config,
                stream_mode="values"
            ):
                yield chunk

        # Yield chunks asynchronously
        for chunk in await loop.run_in_executor(None, lambda: list(stream_gen())):
            yield chunk
            await asyncio.sleep(0)  # Allow UI to update

    @work(exclusive=True)
    async def process_message(self, message: str) -> None:
        """Process message with the agent using streaming."""
        self.status_bar.set_status("Agent is thinking...")

        try:
            # Track processed messages to avoid duplicates
            processed_message_ids = set()
            last_ai_content = ""
            seen_tool_calls = set()

            # Process streaming chunks
            async for chunk in self._stream_agent_response(message):
                # Extract messages from chunk
                if "messages" in chunk and len(chunk["messages"]) > 0:
                    # Process all messages in chunk (in case multiple arrived)
                    for msg in chunk["messages"]:
                        # Generate a message ID to avoid duplicates
                        msg_id = id(msg)
                        if msg_id in processed_message_ids:
                            continue

                        processed_message_ids.add(msg_id)

                        # Handle AI messages with tool calls
                        if hasattr(msg, 'tool_calls') and msg.tool_calls:
                            for tool_call in msg.tool_calls:
                                # Create unique ID for tool call
                                tool_call_id = f"{tool_call.get('name', 'unknown')}_{str(tool_call.get('args', {}))}"
                                if tool_call_id in seen_tool_calls:
                                    continue
                                seen_tool_calls.add(tool_call_id)

                                tool_name = tool_call.get('name', 'unknown')
                                tool_args = tool_call.get('args', {})

                                self.status_bar.set_status(f"Running tool: {tool_name}")

                                # Display tool call
                                tool_display = f"🔧 **Tool Call:** `{tool_name}`\n\n```json\n{self._format_tool_args(tool_args)}\n```"
                                self.messages.write(Panel(
                                    Markdown(tool_display),
                                    title=f"[bold yellow]Tool: {tool_name}[/bold yellow]",
                                    border_style="yellow"
                                ))
                                self.messages.scroll_end()

                        # Handle tool responses
                        elif hasattr(msg, 'type') and msg.type == 'tool':
                            tool_name = getattr(msg, 'name', 'tool')
                            tool_content = msg.content

                            # Truncate long outputs
                            max_length = 500
                            if len(tool_content) > max_length:
                                tool_content = tool_content[:max_length] + f"\n... (truncated, {len(tool_content)} chars total)"

                            self.messages.write(Panel(
                                f"```\n{tool_content}\n```",
                                title=f"[bold blue]Tool Output: {tool_name}[/bold blue]",
                                border_style="blue"
                            ))
                            self.messages.scroll_end()

                        # Handle AI text content (final response)
                        elif hasattr(msg, 'content') and msg.content and hasattr(msg, 'type') and msg.type == 'ai':
                            content = msg.content

                            # Only display if this is new content
                            if content and content != last_ai_content:
                                last_ai_content = content
                                self.status_bar.set_status("Agent responding...")

                                # Display the response
                                self.messages.write(Panel(
                                    Markdown(content),
                                    title="[bold green]🤖 Agent[/bold green]",
                                    border_style="green"
                                ))
                                self.messages.scroll_end()

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
