#!/usr/bin/env python3
"""
vibe-local: Windows ローカルアプリ用のチャット UI
Azure OpenAI または Gemini を使用して、SQLite と Excel ファイルを操作可能。

使用法:
    python vibe_local_chat.py              # チャットモード
    python vibe_local_chat.py --help       # ヘルプ表示
"""

import os
import sys
import json
import argparse
import textwrap
from pathlib import Path

# llm_client と local_tools をインポート
try:
    from llm_client import get_llm_client, AzureOpenAIClient, GeminiClient
    from local_tools import SQLiteTool, ExcelTool
except ImportError as e:
    print(f"Error: Could not import required modules. {e}")
    print("Make sure llm_client.py and local_tools.py are in the same directory.")
    sys.exit(1)


class Config:
    """Application configuration."""
    
    def __init__(self):
        self.max_tokens = 8192
        self.temperature = 0.7
        self.context_window = 32768
        self.debug = False
        
        # Platform-specific data directories
        if os.name == "nt":  # Windows
            appdata = os.environ.get("LOCALAPPDATA")
            if not appdata:
                appdata = os.path.join(os.path.expanduser("~"), "AppData", "Local")
            self.data_dir = os.path.join(appdata, "vibe-local", "data")
            self.excel_dir = os.path.join(appdata, "vibe-local", "excel")
        else:  # Unix-like
            home = os.path.expanduser("~")
            self.data_dir = os.path.join(home, ".local", "share", "vibe-local", "data")
            self.excel_dir = os.path.join(home, ".local", "share", "vibe-local", "excel")
        
        # Create directories
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.excel_dir, exist_ok=True)


class ChatSession:
    """Maintains conversation history and state."""
    
    def __init__(self, client, config):
        self.client = client
        self.config = config
        self.messages = []
        self.system_prompt = self._build_system_prompt()
    
    def _build_system_prompt(self):
        """Build system prompt with tool information."""
        return textwrap.dedent("""
        You are a helpful assistant for Windows local applications.
        You can help with:
        1. Analyzing and querying SQLite databases
        2. Reading and analyzing Excel files
        3. General chat and assistance
        
        Always use the provided tools to access data when requested.
        Keep responses concise and clear.
        """).strip()
    
    def add_user_message(self, content):
        """Add user message to history."""
        self.messages.append({
            "role": "user",
            "content": content
        })
    
    def add_assistant_message(self, content):
        """Add assistant message to history."""
        self.messages.append({
            "role": "assistant",
            "content": content
        })
    
    def get_messages_for_api(self):
        """Get messages in format suitable for API."""
        return [
            {"role": "system", "content": self.system_prompt}
        ] + self.messages
    
    def send_message(self, user_input):
        """Send message and get response."""
        self.add_user_message(user_input)
        
        messages = self.get_messages_for_api()
        tools = self._get_tools_definition()
        
        try:
            response = self.client.chat_sync(
                model="",  # Not used for Azure/Gemini
                messages=messages,
                tools=tools if tools else None
            )
            
            content = response.get("content", "")
            tool_calls = response.get("tool_calls", [])
            
            # Process tool calls if any
            tool_results = []
            for tc in tool_calls:
                tool_result = self._invoke_tool(tc)
                tool_results.append(tool_result)
                
                # Add assistant message with tool calls
                if not content:
                    content = f"Executing: {tc['name']}"
            
            self.add_assistant_message(content)
            
            return {
                "success": True,
                "content": content,
                "tool_calls": tool_calls,
                "tool_results": tool_results
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _invoke_tool(self, tool_call):
        """Invoke a tool based on tool_call definition."""
        tool_name = tool_call.get("name", "")
        arguments = tool_call.get("arguments", {})
        
        try:
            if tool_name == "sqlite_query":
                tool = SQLiteTool(self.config.data_dir)
                result = tool.invoke(**arguments)
                return {
                    "tool": tool_name,
                    "status": "success" if result.exit_code == 0 else "error",
                    "output": result.output,
                    "error": result.error
                }
            elif tool_name == "read_excel":
                tool = ExcelTool(self.config.excel_dir)
                result = tool.invoke(**arguments)
                return {
                    "tool": tool_name,
                    "status": "success" if result.exit_code == 0 else "error",
                    "output": result.output,
                    "error": result.error
                }
            else:
                return {
                    "tool": tool_name,
                    "status": "error",
                    "error": f"Unknown tool: {tool_name}"
                }
        except Exception as e:
            return {
                "tool": tool_name,
                "status": "error",
                "error": str(e)
            }
    
    def _get_tools_definition(self):
        """Get tool definitions for the API."""
        tools = []
        
        # SQLite tool
        sqlite_tool = SQLiteTool(self.config.data_dir)
        tools.append(sqlite_tool.definition)
        
        # Excel tool
        excel_tool = ExcelTool(self.config.excel_dir)
        tools.append(excel_tool.definition)
        
        return tools


def print_banner():
    """Print application banner."""
    banner = textwrap.dedent("""
    ╔════════════════════════════════════════════════════════════════╗
    ║                     vibe-local Chat                           ║
    ║                                                                ║
    ║  Azure OpenAI または Gemini を使用したローカルAIチャット      ║
    ║  SQLite + Excel ファイル対応                                   ║
    ╚════════════════════════════════════════════════════════════════╝
    """)
    print(banner)


def print_help():
    """Print help message."""
    help_text = textwrap.dedent("""
    コマンド:
      /help      - このヘルプを表示
      /quit      - 終了
      /exit      - 終了
      /clear     - 会話をクリア
      /config    - 設定を表示
      
    データ操作:
      SQLite データベースはこちらに配置:
        Windows: %LOCALAPPDATA%\\vibe-local\\data\\
        Linux:   ~/.local/share/vibe-local/data/
      
      Excel ファイルはこちらに配置:
        Windows: %LOCALAPPDATA%\\vibe-local\\excel\\
        Linux:   ~/.local/share/vibe-local/excel/
      
    使用例:
      "app.db の users テーブルの内容を表示して"
      "data.xlsx の最初のシートを読んで"
      "SELECT * FROM products WHERE price > 100 を実行して"
    """)
    print(help_text)


def print_config(config, client):
    """Print current configuration."""
    print("\n" + "="*60)
    print("Configuration")
    print("="*60)
    
    if isinstance(client, AzureOpenAIClient):
        print(f"LLM Provider:    Azure OpenAI")
        print(f"Deployment:      {client.deployment}")
        print(f"Endpoint:        {client.endpoint[:50]}...")
    elif isinstance(client, GeminiClient):
        print(f"LLM Provider:    Google Gemini")
        print(f"Model:           {client.model_name}")
    
    print(f"Max Tokens:      {config.max_tokens}")
    print(f"Temperature:     {config.temperature}")
    print(f"Context Window:  {config.context_window}")
    print(f"\nData Directory:  {config.data_dir}")
    print(f"Excel Directory: {config.excel_dir}")
    print("="*60 + "\n")


def main():
    """Main chat loop."""
    parser = argparse.ArgumentParser(
        description="vibe-local: Local AI chat for Windows",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--temp", type=float, default=0.7, help="Temperature (0-1)")
    parser.add_argument("--max-tokens", type=int, default=8192, help="Max tokens")
    args = parser.parse_args()
    
    # Initialize config
    config = Config()
    config.debug = args.debug
    config.temperature = args.temp
    config.max_tokens = args.max_tokens
    
    # Print banner
    print_banner()
    
    # Get LLM client
    try:
        client = get_llm_client(config)
        ok, models = client.check_connection()
        if not ok:
            print("❌ Error: Could not connect to LLM service.")
            print("Please ensure:")
            print("  1. AZURE_OPENAI_API_KEY + AZURE_OPENAI_ENDPOINT are set (for Azure), OR")
            print("  2. GEMINI_API_KEY is set (for Gemini)")
            sys.exit(1)
        print("✓ LLM service connected successfully\n")
    except RuntimeError as e:
        print(f"❌ Error: {e}\n")
        sys.exit(1)
    
    # Show configuration
    print_config(config, client)
    
    # Initialize chat session
    session = ChatSession(client, config)
    
    print("Type '/help' for available commands, or start chatting.")
    print("Press Ctrl+C to quit.\n")
    
    try:
        while True:
            try:
                user_input = input("You: ").strip()
            except EOFError:
                break
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.startswith("/"):
                cmd = user_input.split()[0].lower()
                
                if cmd in ("/quit", "/exit"):
                    print("Goodbye!")
                    break
                elif cmd == "/help":
                    print_help()
                elif cmd == "/clear":
                    session.messages = []
                    print("✓ Conversation cleared")
                elif cmd == "/config":
                    print_config(config, client)
                else:
                    print(f"❌ Unknown command: {cmd}")
                continue
            
            # Send message
            print("\nAssistant: ", end="", flush=True)
            result = session.send_message(user_input)
            
            if result["success"]:
                print(result["content"])
                
                # Handle tool calls if any
                if result.get("tool_results"):
                    print("\n[Tool Execution Results]")
                    for tool_result in result["tool_results"]:
                        tool_name = tool_result.get("tool", "unknown")
                        status = tool_result.get("status", "unknown")
                        
                        if status == "success":
                            output = tool_result.get("output", "")
                            # Truncate long output
                            if len(output) > 500:
                                output = output[:500] + "\n... (output truncated)"
                            print(f"\n✓ {tool_name}:")
                            print(output)
                        else:
                            error = tool_result.get("error", "Unknown error")
                            print(f"\n✗ {tool_name}:")
                            print(f"  Error: {error}")
            else:
                print(f"❌ Error: {result['error']}")
            
            print()
    
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        if config.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
