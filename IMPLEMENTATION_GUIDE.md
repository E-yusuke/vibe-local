# vibe-local Windows ローカルアプリ改修 - 実装ガイド

## 概要

既存の vibe-coder (Ollama ベース) から、Windows 向けのセキュアなローカルアプリケーションへ改修しました。Azure OpenAI と Google Gemini に対応し、SQLite データベースと Excel ファイル操作が可能です。

## 改修内容

### 1. LLM層の刷新（llm_client.py）

**特徴:**
- Azure OpenAI をデフォルト LLM として採用
- Google Gemini へのフォールバック対応
- カスタムヘッダーサポート
- 環境変数による設定管理

**クラス構成:**

```python
BaseLLMClient (抽象基底クラス)
├── AzureOpenAIClient
│   └── check_connection()
│   └── chat()
│   └── chat_sync()
│   └── _iter_sse()
└── GeminiClient
    └── check_connection()
    └── chat()
    └── chat_sync()
    └── _iter_sse()

get_llm_client(config)  # ファクトリ関数
```

**優先順位:**
1. `AZURE_OPENAI_API_KEY` + `AZURE_OPENAI_ENDPOINT` が設定されていれば Azure OpenAI
2. `GEMINI_API_KEY` が設定されていれば Gemini
3. どちらも設定されていなければエラー

### 2. データベース操作ツール（local_tools.py - SQLiteTool）

**機能:**
- SQL クエリの実行（SELECT, INSERT, UPDATE, DELETE, CREATE TABLE など）
- パラメータ化クエリによる SQL インジェクション防止
- セキュアなエラーメッセージ表示
- パストラバーサル防止

**ツール定義:**

```json
{
  "type": "function",
  "function": {
    "name": "sqlite_query",
    "description": "Execute a SQL query against a SQLite database",
    "parameters": {
      "type": "object",
      "properties": {
        "database": {
          "type": "string",
          "description": "Database filename (without path, e.g., 'app.db')"
        },
        "query": {
          "type": "string",
          "description": "SQL query to execute"
        },
        "params": {
          "type": "array",
          "description": "Parameters for parameterized queries (optional)"
        }
      },
      "required": ["database", "query"]
    }
  }
}
```

**使用例:**
```python
tool = SQLiteTool(db_folder="~/.local/share/vibe-local/data")
result = tool.invoke(
    database="app.db",
    query="SELECT * FROM users WHERE age > ?",
    params=[18]
)
```

### 3. Excel ファイル操作ツール（local_tools.py - ExcelTool）

**機能:**
- `.xlsx` ファイルの読み込み
- 複数シート対応
- データサマリー取得
- シート一覧表示

**ツール定義:**

```json
{
  "type": "function",
  "function": {
    "name": "read_excel",
    "description": "Read and analyze Excel files",
    "parameters": {
      "type": "object",
      "properties": {
        "filename": {
          "type": "string",
          "description": "Excel filename (with .xlsx extension)"
        },
        "sheet": {
          "type": "string",
          "description": "Sheet name (optional, defaults to first sheet)"
        },
        "action": {
          "type": "string",
          "enum": ["list_sheets", "read", "summary"],
          "description": "Action to perform (default: read)"
        },
        "rows": {
          "type": "integer",
          "description": "Number of rows to read (default: all)"
        }
      },
      "required": ["filename"]
    }
  }
}
```

**使用例:**
```python
tool = ExcelTool(excel_folder="~/.local/share/vibe-local/excel")
result = tool.invoke(filename="data.xlsx", action="summary")
```

### 4. チャットアプリケーション（vibe_local_chat.py）

**特徴:**
- シンプルなチャット UI
- ツール呼び出し自動実行
- 会話履歴管理
- コマンドシステム（/help, /quit, /clear など）

**クラス構成:**

```python
Config
├── max_tokens
├── temperature
├── context_window
├── data_dir
└── excel_dir

ChatSession
├── messages[]
├── system_prompt
├── add_user_message()
├── send_message()
├── _invoke_tool()
└── _get_tools_definition()

main()
```

**コマンド一覧:**
- `/help` - ヘルプ表示
- `/quit`, `/exit` - 終了
- `/clear` - 会話クリア
- `/config` - 設定表示

### 5. セットアップスクリプト

**Windows 用バッチファイル:**

1. `install_and_run.bat` - 依存パッケージインストール + アプリ起動
2. `run_chat.bat` - 認証情報確認 + アプリ起動
3. `setup_azure.bat` - Azure OpenAI 環境変数設定（テンプレート）

## ディレクトリ構成

```
vibe-local/
├── vibe_local_chat.py          # メインアプリケーション
├── llm_client.py               # LLM クライアント（Azure/Gemini）
├── local_tools.py              # ツール実装（SQLite/Excel）
├── test_vibe_local.py          # テストスイート
├── requirements.txt            # Python 依存関係
├── setup.py                    # pip インストール用
├── install_and_run.bat         # Windows セットアップ＋実行
├── run_chat.bat                # Windows 起動スクリプト
├── VIBE_LOCAL_README.md        # ユーザードキュメント
├── SETUP_WINDOWS.md            # Windows セットアップガイド
└── このドキュメント
```

## データディレクトリ

```
Windows:
  %LOCALAPPDATA%\vibe-local\
  ├── data\           # SQLite データベースファイル
  └── excel\          # Excel (.xlsx) ファイル

Unix/Linux:
  ~/.local/share/vibe-local/
  ├── data/
  └── excel/
```

## セキュリティ対策

### 1. SQL インジェクション防止
- パラメータ化クエリ使用
- `?` プレースホルダーでクエリパラメータを分離

### 2. パストラバーサル防止
- ファイル名検証（`/`, `\`, `.` を含む名前を拒否）
- 絶対パスで許可フォルダ内のみアクセス
- 実装例:
  ```python
  real_path = os.path.abspath(db_path)
  real_folder = os.path.abspath(self.db_folder)
  if not real_path.startswith(real_folder):
      raise SecurityError()
  ```

### 3. API キー管理
- 環境変数による設定（バッチファイルにハードコードしない）
- ログに API キーを出力しない
- HTTPS のみを使用

### 4. 入力検証
- SQL クエリの長さ制限
- 応答サイズの上限設定
- 不正なデータベース名の拒否

## テスト

`test_vibe_local.py` でコンポーネント単体テストを実施：

```bash
python test_vibe_local.py
```

**テスト項目:**
1. LLM クライアント初期化
2. SQLite クエリ実行
3. Excel ファイル読み込み
4. Config 初期化
5. セキュリティ防止機能

## 使用フロー

```
ユーザー
  ↓
vibe_local_chat.py (チャットUI)
  ↓
ChatSession
  ├→ LLM API (Azure OpenAI / Gemini)
  │   ├→ Tool 実行判定
  │   └→ ツール呼び出し
  │
  └→ Tool 実行
      ├→ SQLiteTool
      │   └→ SQLite (user data)
      │
      └→ ExcelTool
          └→ Excel (user files)
```

## 拡張性

新しいツールを追加する手順：

1. `local_tools.py` で `Tool` クラスを継承
2. `definition` プロパティで OpenAI 互換スキーマを定義
3. `invoke()` メソッドを実装
4. `ChatSession._get_tools_definition()` に追加

```python
class CustomTool(Tool):
    @property
    def definition(self):
        return {
            "type": "function",
            "function": {
                "name": "custom_tool",
                "description": "...",
                "parameters": {...}
            }
        }
    
    def invoke(self, **kwargs):
        # 実装
        return ToolResult(output="...", error="")
```

## 非対応事項

- **CLI 実行機能**: セキュリティ上の理由から非対応（chats only）
- **オンプレミス LLM**: Ollama や LocalAI は非対応（API ベースのみ）
- **Streaming ツール呼び出し**: 実装未対応（同期処理のみ）

## 環境変数リファレンス

### Azure OpenAI

```
AZURE_OPENAI_API_KEY=<your-api-key>
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_DEPLOYMENT=gpt-4-turbo
AZURE_OPENAI_API_VERSION=2024-08-01-preview
```

### Google Gemini

```
GEMINI_API_KEY=<your-api-key>
GEMINI_MODEL=gemini-2.0-flash
```

## トラブルシューティング

### "No module named 'pandas'"
```bash
pip install pandas openpyxl
```

### "Connection refused to LLM service"
- API キーが正しく設定されているか確認
- インターネット接続を確認
- LLM サービスが正常に動作しているか確認

### "Database file not found"
- ファイルが `%LOCALAPPDATA%\vibe-local\data\` に存在するか確認
- ファイル名に拡張子 `.db` があるか確認

### "Invalid Excel file"
- ファイル形式が `.xlsx` か確認（`.xls` は非対応）
- Excel ファイルが破損していないか確認

## ライセンス

MIT License

## 更新予定

- v1.1.0: JSON/CSV データサポート追加
- v1.2.0: データ可視化機能（グラフ生成）
- v1.3.0: 複数ユーザーサポート
