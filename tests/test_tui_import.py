#!/usr/bin/env python
"""
Simple import test for the TUI module.
"""
import sys

def test_imports():
    """Test that all TUI components can be imported."""
    try:
        print("Testing TUI imports...")

        # Test main TUI module import
        from buddycode.tui import BuddyCodeTUI, main
        print("✓ buddycode.tui imported successfully")

        # Test Textual imports
        from textual.app import App
        print("✓ Textual imported successfully")

        # Test agent import
        from buddycode.react_agent import create_coding_agent
        print("✓ react_agent imported successfully")

        # Test that the app class is properly defined
        assert issubclass(BuddyCodeTUI, App)
        print("✓ BuddyCodeTUI is a valid Textual App")

        # Test that main is callable
        assert callable(main)
        print("✓ main() function is callable")

        print("\n✅ All imports successful!")
        print("🎉 TUI is ready to run!")
        print("\nTo launch the TUI:")
        print("  uv run python -m buddycode.tui")
        print("  or: uv run python test_tui.py")

        return 0

    except Exception as e:
        print(f"\n❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(test_imports())
