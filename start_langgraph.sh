#!/bin/bash
#
# LangGraph Development Server Startup Script
#
# This script starts the LangGraph development server for the coding agent.
# The server provides a REST API for interacting with the agent.
#

# Set colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}======================================================================${NC}"
echo -e "${BLUE}LangGraph Development Server - BuddyCode Coding Agent${NC}"
echo -e "${BLUE}======================================================================${NC}"
echo ""

# Check if langgraph-cli is installed
if ! command -v langgraph &> /dev/null && ! uv run langgraph --version &> /dev/null; then
    echo -e "${YELLOW}⚠️  LangGraph CLI not found. Installing...${NC}"
    uv pip install -U "langgraph-cli[inmem]"
fi

# Default port
PORT=${1:-8123}

echo -e "${GREEN}🚀 Starting LangGraph dev server on port ${PORT}...${NC}"
echo -e "${GREEN}📡 API will be available at: http://localhost:${PORT}${NC}"
echo -e "${GREEN}📊 Studio URL: https://smith.langchain.com${NC}"
echo ""
echo -e "${YELLOW}💡 Available endpoints:${NC}"
echo -e "   - GET  /info        - Server information"
echo -e "   - GET  /assistants  - List available assistants"
echo -e "   - POST /runs/create - Create a new run"
echo ""
echo -e "${YELLOW}🛑 Press Ctrl+C to stop the server${NC}"
echo ""

# Start the server
uv run langgraph dev --port $PORT --no-browser
