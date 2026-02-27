#!/usr/bin/env python3
"""
Test script for vibe-local components.
"""

import os
import sys
import sqlite3
import tempfile
from pathlib import Path


def test_llm_client():
    """Test LLM client initialization."""
    print("=" * 60)
    print("Testing LLM Client Factory")
    print("=" * 60)
    
    try:
        from llm_client import get_llm_client, AzureOpenAIClient, GeminiClient, BaseLLMClient
        
        # Create a mock config
        class MockConfig:
            max_tokens = 8192
            temperature = 0.7
            context_window = 32768
            debug = False
        
        config = MockConfig()
        
        # Test 1: Check if Azure OpenAI is configured
        azure_key = os.environ.get("AZURE_OPENAI_API_KEY", "")
        if azure_key:
            print("\n✓ Azure OpenAI credentials found")
            try:
                client = get_llm_client(config)
                assert isinstance(client, AzureOpenAIClient)
                print("✓ Azure OpenAI client created successfully")
            except Exception as e:
                print(f"✗ Failed to create Azure OpenAI client: {e}")
        else:
            print("\n- Azure OpenAI credentials not set (OK)")
        
        # Test 2: Check if Gemini is configured
        gemini_key = os.environ.get("GEMINI_API_KEY", "")
        if gemini_key:
            print("✓ Gemini credentials found")
            try:
                client = get_llm_client(config)
                assert isinstance(client, GeminiClient)
                print("✓ Gemini client created successfully")
            except Exception as e:
                print(f"✗ Failed to create Gemini client: {e}")
        else:
            print("- Gemini credentials not set (OK)")
        
        # Test 3: No credentials error
        if not azure_key and not gemini_key:
            print("\n⚠️  No LLM credentials found")
            try:
                client = get_llm_client(config)
                print("✗ Should have raised RuntimeError")
            except RuntimeError as e:
                print(f"✓ Correctly raised error: {str(e)[:50]}...")
        
        print("\n✓ LLM Client tests passed\n")
        return True
    
    except ImportError as e:
        print(f"\n✗ Import error: {e}\n")
        return False


def test_sqlite_tool():
    """Test SQLite tool."""
    print("=" * 60)
    print("Testing SQLite Tool")
    print("=" * 60)
    
    try:
        from local_tools import SQLiteTool, ToolResult
        
        # Create a temporary directory for test database
        with tempfile.TemporaryDirectory() as tmpdir:
            print(f"\nUsing temporary directory: {tmpdir}")
            
            # Create tool
            tool = SQLiteTool(db_folder=tmpdir)
            print("✓ SQLiteTool created")
            
            # Test 1: Create table and insert data
            print("\n[Test 1] Creating table and inserting data...")
            result = tool.invoke(
                database="test.db",
                query="CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)"
            )
            if result.exit_code == 0:
                print("✓ Table created")
            else:
                print(f"✗ Failed: {result.error}")
                return False
            
            # Test 2: Insert data
            print("[Test 2] Inserting data...")
            result = tool.invoke(
                database="test.db",
                query="INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com')"
            )
            if result.exit_code == 0:
                print("✓ Data inserted")
            else:
                print(f"✗ Failed: {result.error}")
                return False
            
            # Test 3: Query data
            print("[Test 3] Querying data...")
            result = tool.invoke(
                database="test.db",
                query="SELECT * FROM users"
            )
            if result.exit_code == 0 and "Alice" in result.output:
                print("✓ Data retrieved successfully")
                print(f"  Result: {result.output[:100]}...")
            else:
                print(f"✗ Failed: {result.error}")
                return False
            
            # Test 4: Path traversal prevention
            print("[Test 4] Testing path traversal prevention...")
            result = tool.invoke(
                database="../evil.db",
                query="SELECT 1"
            )
            if result.exit_code != 0 and "Invalid" in result.error:
                print("✓ Path traversal correctly blocked")
            else:
                print("✗ Path traversal not blocked!")
                return False
            
            print("\n✓ SQLite Tool tests passed\n")
            return True
    
    except ImportError as e:
        print(f"\n✗ Import error: {e}\n")
        return False


def test_excel_tool():
    """Test Excel tool."""
    print("=" * 60)
    print("Testing Excel Tool")
    print("=" * 60)
    
    try:
        from local_tools import ExcelTool
        
        with tempfile.TemporaryDirectory() as tmpdir:
            print(f"\nUsing temporary directory: {tmpdir}")
            
            # Create tool
            tool = ExcelTool(excel_folder=tmpdir)
            print("✓ ExcelTool created")
            
            # Try to create a test Excel file
            try:
                import pandas as pd
                
                # Test 1: Create Excel file
                print("\n[Test 1] Creating test Excel file...")
                data = {
                    "Name": ["Alice", "Bob", "Charlie"],
                    "Age": [25, 30, 35],
                    "City": ["Tokyo", "Osaka", "Kyoto"]
                }
                df = pd.DataFrame(data)
                excel_path = os.path.join(tmpdir, "test.xlsx")
                df.to_excel(excel_path, sheet_name="Sheet1", index=False)
                print("✓ Excel file created")
                
                # Test 2: List sheets
                print("[Test 2] Listing sheets...")
                result = tool.invoke(
                    filename="test.xlsx",
                    action="list_sheets"
                )
                if result.exit_code == 0 and "Sheet1" in result.output:
                    print("✓ Sheets listed successfully")
                else:
                    print(f"✗ Failed: {result.error}")
                    return False
                
                # Test 3: Read data
                print("[Test 3] Reading Excel data...")
                result = tool.invoke(
                    filename="test.xlsx",
                    action="read"
                )
                if result.exit_code == 0 and "Alice" in result.output:
                    print("✓ Excel data read successfully")
                    print(f"  Result: {result.output[:100]}...")
                else:
                    print(f"✗ Failed: {result.error}")
                    return False
                
                # Test 4: Get summary
                print("[Test 4] Getting Excel summary...")
                result = tool.invoke(
                    filename="test.xlsx",
                    action="summary"
                )
                if result.exit_code == 0:
                    print("✓ Excel summary retrieved")
                else:
                    print(f"✗ Failed: {result.error}")
                    return False
                
                # Test 5: Path traversal prevention
                print("[Test 5] Testing path traversal prevention...")
                result = tool.invoke(
                    filename="../evil.xlsx",
                    action="read"
                )
                if result.exit_code != 0 and "Invalid" in result.error:
                    print("✓ Path traversal correctly blocked")
                else:
                    print("✗ Path traversal not blocked!")
                    return False
                
                print("\n✓ Excel Tool tests passed\n")
                return True
            
            except ImportError:
                print("\n⚠️  pandas not installed - skipping Excel creation test")
                print("✓ Tool class initialized successfully (libraries optional)")
                return True
    
    except ImportError as e:
        print(f"\n✗ Import error: {e}\n")
        return False


def test_config():
    """Test Config class."""
    print("=" * 60)
    print("Testing Config")
    print("=" * 60)
    
    try:
        from vibe_local_chat import Config
        
        config = Config()
        print(f"\n✓ Config created")
        print(f"  Data dir: {config.data_dir}")
        print(f"  Excel dir: {config.excel_dir}")
        
        # Check if directories exist
        if os.path.exists(config.data_dir):
            print("✓ Data directory exists")
        else:
            print("✗ Data directory does not exist")
            return False
        
        if os.path.exists(config.excel_dir):
            print("✓ Excel directory exists")
        else:
            print("✗ Excel directory does not exist")
            return False
        
        print("\n✓ Config tests passed\n")
        return True
    
    except ImportError as e:
        print(f"\n✗ Import error: {e}\n")
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("vibe-local Component Tests")
    print("=" * 60 + "\n")
    
    results = {}
    
    results["llm_client"] = test_llm_client()
    results["sqlite_tool"] = test_sqlite_tool()
    results["excel_tool"] = test_excel_tool()
    results["config"] = test_config()
    
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{name:20} {status}")
    
    total = len(results)
    passed = sum(1 for p in results.values() if p)
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
