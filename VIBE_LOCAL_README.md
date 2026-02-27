# vibe-local チャット (Windows ローカルアプリ版)

Windows 環境で Azure OpenAI または Google Gemini を使用したローカル AI チャットアプリケーションです。SQLite データベースと Excel ファイルを直接操作できます。

## 特徴

- **LLM の柔軟性**: Azure OpenAI（デフォルト）と Google Gemini に対応
- **データアクセス**: SQLite DB の SQL クエリ実行、Excel ファイルの読み込み
- **追加ソフトウェア不要**: Python と pip でのみ実行可能（社内環境対応）
- **チャット専用**: CLI 実行機能なし、セキュアな操作

## システム要件

- Windows 10/11 以上
- Python 3.8 以上
- インターネット接続（LLM API 呼び出し用）

## インストール方法

### 1. 初期セットアップ

```bash
# 依存パッケージをインストール
pip install -r requirements.txt
```

または、`install_and_run.bat` をダブルクリック実行：
```cmd
install_and_run.bat
```

### 2. API 認証情報の設定

#### Option A: Azure OpenAI を使用する場合（推奨）

```cmd
# Windows のシステム環境変数として設定
set AZURE_OPENAI_API_KEY=your_api_key_here
set AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
set AZURE_OPENAI_DEPLOYMENT=gpt-4-turbo
set AZURE_OPENAI_API_VERSION=2024-08-01-preview
```

または、`.bat` ファイルで自動設定：
```cmd
@echo off
setx AZURE_OPENAI_API_KEY your_api_key_here
setx AZURE_OPENAI_ENDPOINT https://your-resource.openai.azure.com
setx AZURE_OPENAI_DEPLOYMENT gpt-4-turbo
```

#### Option B: Google Gemini を使用する場合

```cmd
set GEMINI_API_KEY=your_api_key_here
set GEMINI_MODEL=gemini-2.0-flash
```

### 3. アプリケーション実行

#### 方法 1: バッチファイルから（推奨）

```bash
run_chat.bat
```

#### 方法 2: Python コマンドラインから

```bash
python vibe_local_chat.py
```

オプション:
- `--debug`: デバッグモード有効化
- `--temp 0.5`: 生成温度を設定（0-1）
- `--max-tokens 4096`: 最大トークン数を設定

## データディレクトリ構成

アプリケーション実行時に自動生成：

```
%LOCALAPPDATA%\vibe-local\
├── data\              # SQLite データベースファイル
│   ├── app.db
│   ├── users.db
│   └── ...
└── excel\             # Excel ファイル
    ├── data.xlsx
    ├── analysis.xlsx
    └── ...
```

**Unix/Linux:**
```
~/.local/share/vibe-local/
├── data/
└── excel/
```

## 使用方法

### 基本的なチャット

```
You: Azure OpenAI を使ってますか？
Assistant: はい、デフォルトは Azure OpenAI です。ただし Gemini API キーを設定すれば...
```

### SQLite クエリ実行

1. データベースファイルを `%LOCALAPPDATA%\vibe-local\data\` に配置
2. チャットで問い合わせ：

```
You: app.db の users テーブル内容を表示して
You: SELECT * FROM products WHERE price > 100 を実行して
You: customers テーブルのカウントを取ってください
```

### Excel ファイル読み込み

1. Excel ファイルを `%LOCALAPPDATA%\vibe-local\excel\` に配置
2. チャットで問い合わせ：

```
You: sales.xlsx の最初のシートを読んで
You: data.xlsx の Sheet2 に何が入ってますか？
You: analysis.xlsx の概要を表示して
```

### コマンド一覧

```
/help       - ヘルプを表示
/quit       - アプリを終了
/exit       - アプリを終了
/clear      - 会話履歴をクリア
/config     - 現在の設定を表示
```

## トラブルシューティング

### "API credentials not found" エラー

**原因**: Azure OpenAI または Gemini の API キーが設定されていない

**解決方法**:
```cmd
# Azure OpenAI の場合
setx AZURE_OPENAI_API_KEY "your_key"
setx AZURE_OPENAI_ENDPOINT "https://your-resource.openai.azure.com"

# または Gemini の場合
setx GEMINI_API_KEY "your_key"
```

### "pandas/openpyxl not installed" エラー

```bash
pip install pandas openpyxl
```

### SQLite ファイルが見つからない

- ファイルが `%LOCALAPPDATA%\vibe-local\data\` に存在することを確認
- ファイル名が正しい拡張子 (`.db`) を持っているか確認

### Excel ファイルが読めない

- ファイル形式が `.xlsx` であることを確認（`.xls` はサポート外）
- ファイルが `%LOCALAPPDATA%\vibe-local\excel\` に存在することを確認
- Excel がロックしている場合は、一度閉じてから試す

## セキュリティ上の注意

1. **API キー管理**: API キーを .bat ファイルに直接記述しないこと
2. **データベースアクセス**: SQL インジェクション対策済み（パラメータ化クエリ使用）
3. **ファイルアクセス**: パストラバーサル対策済み（許可フォルダ内のみアクセス）
4. **環境変数**: Windows システム環境変数として設定（ユーザースコープ）

## Azure OpenAI 設定例

```powershell
# PowerShell での設定
$env:AZURE_OPENAI_API_KEY = "your-api-key"
$env:AZURE_OPENAI_ENDPOINT = "https://your-resource.openai.azure.com"
$env:AZURE_OPENAI_DEPLOYMENT = "gpt-4-turbo"

# 永続化
[Environment]::SetEnvironmentVariable("AZURE_OPENAI_API_KEY", "your-key", "User")
[Environment]::SetEnvironmentVariable("AZURE_OPENAI_ENDPOINT", "https://...", "User")
[Environment]::SetEnvironmentVariable("AZURE_OPENAI_DEPLOYMENT", "gpt-4-turbo", "User")
```

## Google Gemini 設定例

```bash
# PowerShell での設定
$env:GEMINI_API_KEY = "your-api-key"
$env:GEMINI_MODEL = "gemini-2.0-flash"

# 永続化
[Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "your-key", "User")
[Environment]::SetEnvironmentVariable("GEMINI_MODEL", "gemini-2.0-flash", "User")
```

## 機能一覧

### LLM サポート

- ✅ Azure OpenAI（デフォルト、フォールバック先なし）
- ✅ Google Gemini（Azure キーがない場合のフォールバック）
- ✅ カスタムヘッダー対応
- ✅ ストリーミング応答
- ✅ ツール呼び出し（SQLite/Excel クエリ）

### データベース機能

- ✅ SQLite 接続
- ✅ SELECT/INSERT/UPDATE/DELETE クエリ実行
- ✅ CREATE TABLE などの DDL 実行
- ✅ パラメータ化クエリでの SQL インジェクション防止

### Excel 機能

- ✅ `.xlsx` ファイル読み込み
- ✅ 複数シート対応
- ✅ データ形式の自動判定
- ✅ JSON 形式でのデータ出力

### チャット機能

- ✅ 会話履歴管理
- ✅ システムプロンプト設定可能
- ✅ トークン数制御
- ✅ 温度（temperature）調整可能

## ライセンス

MIT License

## サポート

問題が発生した場合：
1. `/config` コマンドで設定を確認
2. `--debug` フラグで詳細ログを表示
3. API キーの有効性を確認
4. インターネット接続を確認

## 更新情報

### v1.0.0
- 初版リリース
- Azure OpenAI + Gemini 対応
- SQLite + Excel ツール実装
- Windows 専用バッチスクリプト提供
