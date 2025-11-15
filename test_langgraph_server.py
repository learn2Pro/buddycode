#!/usr/bin/env python
"""
Test LangGraph Server

Quick test to verify the LangGraph dev server is running correctly.
"""
import requests
import json

BASE_URL = "http://localhost:8123"

def test_server():
    print("=" * 70)
    print("Testing LangGraph Development Server")
    print("=" * 70)

    # Test 1: Server info
    print("\n[1/2] Testing server info endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/info")
        if response.status_code == 200:
            info = response.json()
            print(f"✓ Server is running!")
            print(f"  Version: {info['version']}")
            print(f"  LangGraph Python: {info['langgraph_py_version']}")
        else:
            print(f"✗ Unexpected status: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

    # Test 2: List assistants
    print("\n[2/2] Checking for coding_agent...")
    try:
        # The endpoint might be /assistants/search with POST
        response = requests.post(
            f"{BASE_URL}/assistants/search",
            json={}
        )
        if response.status_code == 200:
            assistants = response.json()
            print(f"✓ Found {len(assistants)} assistant(s)")
            for assistant in assistants:
                print(f"  - {assistant.get('assistant_id', 'unknown')}")
                if assistant.get('assistant_id') == 'coding_agent':
                    print("    ✓ coding_agent is registered!")
        else:
            print(f"  Status: {response.status_code}")
    except Exception as e:
        print(f"  Note: {e}")

    print("\n" + "=" * 70)
    print("Server Test Complete!")
    print("=" * 70)
    print(f"\n📚 API Documentation: {BASE_URL}/docs")
    print(f"🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl={BASE_URL}")
    print("\n✅ LangGraph server is running successfully!")
    return True

if __name__ == "__main__":
    test_server()
