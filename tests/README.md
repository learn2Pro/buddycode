# BuddyCode TUI Tests

Comprehensive test suite for the BuddyCode Text User Interface.

## Test Structure

```
tests/
├── __init__.py                    # Package marker
├── conftest.py                    # Pytest fixtures and configuration
├── test_tui_comprehensive.py      # Main functionality tests (24 tests)
├── test_tui_edge_cases.py         # Edge cases and stress tests (18 tests)
├── test_tui_widgets.py            # Widget-specific tests (16 tests)
├── test_tui_streaming.py          # Streaming features tests (6 tests)
└── README.md                      # This file
```

**Total: 94 tests**

## Test Coverage

### test_tui_comprehensive.py
- Widget initialization and composition
- Status bar updates
- Message handling
- User input processing
- Agent integration (mocked)
- Error handling
- Action bindings (clear, quit)
- Async operations
- Full conversation flows

### test_tui_edge_cases.py
- Very long inputs
- Special characters (unicode, emojis, symbols)
- Whitespace-only inputs
- Rapid message submission
- Agent response edge cases
- Timeout simulation
- Markdown rendering
- Various exception types
- Stress tests with many messages

### test_tui_widgets.py
- MessageDisplay widget behavior
- StatusBar widget behavior
- Widget integration
- CSS and styling
- Message writing and clearing
- Status updates

### test_tui_streaming.py
- Tool call display (blue panels)
- Tool result display (cyan panels)
- Thinking display (yellow panels)
- Multiple sequential tool calls
- Tool argument formatting
- Long output truncation
- Status bar updates during tool execution

## Running Tests

### Run all tests
```bash
# Using pytest directly
pytest tests/

# Using uv
uv run pytest tests/

# With verbose output
pytest tests/ -v

# With coverage
pytest tests/ --cov=buddycode.tui --cov-report=html
```

### Run specific test files
```bash
pytest tests/test_tui_comprehensive.py
pytest tests/test_tui_edge_cases.py
pytest tests/test_tui_widgets.py
```

### Run specific test classes or functions
```bash
# Run a specific test class
pytest tests/test_tui_comprehensive.py::TestBuddyCodeTUI

# Run a specific test function
pytest tests/test_tui_comprehensive.py::TestBuddyCodeTUI::test_app_creation

# Run tests matching a pattern
pytest tests/ -k "test_agent"
```

### Run with markers
```bash
# Run only fast tests
pytest tests/ -m "not slow"

# Run only integration tests
pytest tests/ -m "integration"
```

## Test Requirements

Install test dependencies:
```bash
uv pip install -e ".[dev]"
# or
pip install pytest pytest-asyncio pytest-cov
```

## Writing New Tests

### Basic Test Template
```python
import pytest
from buddycode.tui import BuddyCodeTUI

@pytest.mark.asyncio
async def test_my_feature():
    """Test description."""
    app = BuddyCodeTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        # Your test code here
        assert something
```

### Using Fixtures
```python
def test_with_mock_agent(mock_agent):
    """Use the mock_agent fixture."""
    result = mock_agent.invoke({"messages": [("user", "test")]})
    assert "messages" in result
```

### Testing Async Behavior
```python
@pytest.mark.asyncio
async def test_async_feature():
    """Test async behavior."""
    app = BuddyCodeTUI()
    async with app.run_test() as pilot:
        # Pause to let async operations complete
        await pilot.pause(0.5)

        # Test your feature
        assert app.agent is not None
```

## Best Practices

1. **Use fixtures** from `conftest.py` for common test data
2. **Mock external dependencies** (agent, file system, etc.)
3. **Test edge cases** (empty input, very long input, special chars)
4. **Use async properly** - await pilot.pause() when needed
5. **Clean up** - tests should not affect each other
6. **Descriptive names** - test names should explain what they test
7. **Good assertions** - assert specific conditions, not just "no crash"

## CI/CD Integration

These tests are designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Run tests
  run: |
    uv pip install -e ".[dev]"
    pytest tests/ -v --cov=buddycode.tui
```

## Debugging Failed Tests

### Run with more output
```bash
pytest tests/ -vv -s
```

### Run with pdb debugger
```bash
pytest tests/ --pdb
```

### Show captured output
```bash
pytest tests/ --capture=no
```

## Coverage Reports

Generate and view coverage:
```bash
# Generate HTML coverage report
pytest tests/ --cov=buddycode.tui --cov-report=html

# Open in browser
open htmlcov/index.html
```

## Contributing

When adding new features to the TUI:
1. Write tests first (TDD)
2. Ensure all existing tests pass
3. Add edge case tests
4. Update this README if adding new test files
