# Deployment Guide

## LangGraph Cloud/Platform Deployment

This project includes a `langgraph.json` configuration file for deploying the coding agent with LangGraph Cloud or LangGraph Platform.

### Configuration Files

- **langgraph.json**: Main configuration file defining the agent graph
- **.env.example**: Template for environment variables
- **.env**: Your actual environment variables (git-ignored)

### Setup

1. **Install Dependencies**

   ```bash
   uv sync
   ```

2. **Configure Environment Variables**

   Copy the example environment file and add your API key:

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and set your ByteDance ARK API key:

   ```
   ARK_API_KEY=your-actual-api-key-here
   ```

3. **Test Locally**

   Before deploying, test the agent locally:

   ```bash
   # Run interactive agent
   uv run python src/buddycode/react_agent.py

   # Run tests
   uv run python test_tools.py
   uv run python test_agent_quick.py
   ```

### LangGraph Configuration

The `langgraph.json` file defines:

```json
{
  "dependencies": ["."],
  "graphs": {
    "coding_agent": "./src/buddycode/react_agent.py:create_coding_agent"
  },
  "env": ".env"
}
```

- **dependencies**: Installs the current package (buddycode)
- **graphs**: Maps `coding_agent` to the `create_coding_agent()` function
- **env**: Points to environment variables file

### Deployment with LangGraph CLI

1. **Install LangGraph CLI**

   ```bash
   pip install langgraph-cli
   ```

2. **Test Configuration**

   ```bash
   langgraph test
   ```

3. **Deploy to LangGraph Cloud**

   ```bash
   langgraph deploy
   ```

   Or with LangSmith:

   ```bash
   langgraph up
   ```

### Using the Deployed Agent

Once deployed, you can interact with the agent via:

1. **LangGraph Studio**: Visual interface for testing
2. **API Endpoints**: HTTP/REST API
3. **LangChain SDK**: Programmatic access

Example API usage:

```python
from langgraph_sdk import get_client

client = get_client(url="your-deployment-url")

# Invoke the agent
result = await client.runs.create(
    assistant_id="coding_agent",
    thread_id="user_123",
    input={"messages": [("user", "创建一个 Button 组件")]}
)
```

### Environment Variables

The agent supports the following environment variables:

| Variable       | Description                          | Default                                        |
| -------------- | ------------------------------------ | ---------------------------------------------- |
| ARK_API_KEY    | ByteDance ARK API key                | Hardcoded dev key (replace for production)     |
| ARK_BASE_URL   | ARK API base URL                     | https://ark-cn-beijing.bytedance.net/api/v3    |
| ARK_MODEL      | Model endpoint ID                    | ep-20251010103732-rchjc                        |

### Tools Available

The agent has access to 6 tools:

1. **ls** - List directory contents
2. **grep** - Search for patterns in files
3. **tree** - Display directory structure
4. **bash** - Execute bash commands
5. **text_editor** - View and edit text files
6. **todo** - Manage todo lists

### Memory & Conversations

The agent uses `InMemorySaver` for multi-turn conversations. Each conversation is isolated by `thread_id`:

```python
config = {"configurable": {"thread_id": "user_123"}}
result = agent.invoke({"messages": [("user", "query")]}, config)
```

### Security Notes

- **Never commit `.env` files** to version control (already in `.gitignore`)
- Replace the default API key with your own for production
- Consider using LangGraph Cloud's built-in secrets management for production deployments
- The agent can execute bash commands - ensure proper sandboxing in production

### Troubleshooting

**Import errors:**
```bash
# Ensure package is installed in editable mode
uv pip install -e .
```

**API key issues:**
```bash
# Verify environment variables are loaded
python -c "import os; print(os.getenv('ARK_API_KEY'))"
```

**LangGraph deployment issues:**
```bash
# Check configuration
langgraph test

# View logs
langgraph logs
```

### Additional Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangGraph Cloud](https://www.langchain.com/langgraph-cloud)
- [ByteDance ARK Platform](https://www.volcengine.com/docs/82379)
