#!/usr/bin/env python
"""
Pytest configuration and fixtures for BuddyCode TUI tests.
"""
import pytest
from unittest.mock import Mock


@pytest.fixture
def mock_agent():
    """Create a mock agent for testing."""
    agent = Mock()
    mock_message = Mock()
    mock_message.content = "Test response from agent"
    agent.invoke.return_value = {"messages": [mock_message]}
    return agent


@pytest.fixture
def mock_agent_error():
    """Create a mock agent that raises errors."""
    agent = Mock()
    agent.invoke.side_effect = Exception("Test error")
    return agent


@pytest.fixture
def mock_agent_no_response():
    """Create a mock agent that returns empty messages."""
    agent = Mock()
    agent.invoke.return_value = {"messages": []}
    return agent


@pytest.fixture
def sample_user_messages():
    """Sample user messages for testing."""
    return [
        "Show me the project structure",
        "Find all TODO comments",
        "Help me fix a bug",
        "Create a new file",
        "List all Python files",
    ]


@pytest.fixture
def sample_markdown_content():
    """Sample markdown content for testing rendering."""
    return """
# Test Header

This is a test message with **bold** and *italic* text.

## Code Example

```python
def hello_world():
    print("Hello, World!")
```

## List

- Item 1
- Item 2
- Item 3

## Links

[BuddyCode](https://github.com/example/buddycode)
"""


@pytest.fixture
def complex_agent_responses():
    """Complex agent responses for testing."""
    return [
        {
            "messages": [Mock(content="Simple response")]
        },
        {
            "messages": [
                Mock(content="## Found 3 files\n\n- file1.py\n- file2.py\n- file3.py")
            ]
        },
        {
            "messages": [
                Mock(content="```python\ndef example():\n    pass\n```")
            ]
        },
    ]


@pytest.fixture(autouse=True)
def reset_environment(monkeypatch):
    """Reset environment before each test."""
    # Set any environment variables needed for tests
    monkeypatch.setenv("TESTING", "1")


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "ui: marks tests as UI tests requiring visual verification"
    )
