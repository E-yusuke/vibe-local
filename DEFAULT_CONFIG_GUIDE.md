# API キーのデフォルト設定ガイド

`vibe-local` EXE をビルドする際に、API キーやエンドポイントなどのデフォルト値を埋め込むことができます。

## 概要

デフォルト設定を使用すると、ユーザーが環境変数を設定しなくても、事前に設定されたクレデンシャルで自動的にアプリが起動します。

### 2つの方法

1. **開発者向け**: `default_config.py` を直接編集してハードコード
2. **運用向け**: ビルド時に環境変数で設定

## 方法1: default_config.py を直接編集（簡単）

### ステップ 1: default_config.py を編集

```python
# default_config.py
DEFAULT_AZURE_API_KEY = "sk-abc123xyz..."
DEFAULT_AZURE_ENDPOINT = "https://your-resource.openai.azure.com"
DEFAULT_AZURE_DEPLOYMENT = "gpt-4-turbo"
DEFAULT_AZURE_API_VERSION = "2024-08-01-preview"
```

### ステップ 2: build_exe.bat を実行

```cmd
build_exe.bat
```

デフォルト設定が EXE に埋め込まれます。

### ステップ 3: ユーザーが EXE を実行

```cmd
vibe-local.exe
```

デフォルト設定が自動的に使用されます。

---

## 方法2: ビルド時に環境変数で設定（推奨）

Windows のビルド環境で環境変数を設定してから EXE をビルドします。

### ステップ 1: 環境変数を設定

PowerShell または CMD で以下を実行：

#### PowerShell での設定

```powershell
# Azure OpenAI の場合
[Environment]::SetEnvironmentVariable("DEFAULT_AZURE_API_KEY", "sk-abc123xyz...", "Process")
[Environment]::SetEnvironmentVariable("DEFAULT_AZURE_ENDPOINT", "https://your-resource.openai.azure.com", "Process")
[Environment]::SetEnvironmentVariable("DEFAULT_AZURE_DEPLOYMENT", "gpt-4-turbo", "Process")

# または Gemini の場合
[Environment]::SetEnvironmentVariable("DEFAULT_GEMINI_API_KEY", "your-gemini-key", "Process")
[Environment]::SetEnvironmentVariable("DEFAULT_GEMINI_MODEL", "gemini-2.0-flash", "Process")
```

#### CMD での設定

```cmd
REM 一時的に設定（このCMDセッション内のみ）
set DEFAULT_AZURE_API_KEY=sk-abc123xyz...
set DEFAULT_AZURE_ENDPOINT=https://your-resource.openai.azure.com
set DEFAULT_AZURE_DEPLOYMENT=gpt-4-turbo

REM または永続的に設定（システム全体）
setx DEFAULT_AZURE_API_KEY "sk-abc123xyz..."
setx DEFAULT_AZURE_ENDPOINT "https://your-resource.openai.azure.com"
setx DEFAULT_AZURE_DEPLOYMENT "gpt-4-turbo"
```

### ステップ 2: build_exe.bat を実行

同じ環境変数が設定されている状態で：

```cmd
build_exe.bat
```

### ステップ 3: 自動適用

ビルド時に環境変数から `default_config.py` に自動的に値が適用されます（このステップは今後のバージョンで自動化予定）。

現在は、手動で `default_config.py` を編集する必要があります：

```python
# default_config.py
DEFAULT_AZURE_API_KEY = "sk-abc123xyz..."
DEFAULT_AZURE_ENDPOINT = "https://your-resource.openai.azure.com"
DEFAULT_AZURE_DEPLOYMENT = "gpt-4-turbo"
```

---

## 優先順位

アプリが起動するとき、以下の優先順位でクレデンシャルが使用されます：

1. **ユーザーが設定した環境変数** ← 最優先
2. **default_config.py のデフォルト値**
3. **設定されていない** ← アプリはエラーを出して終了

**重要**: ユーザーが環境変数を設定すれば、それがデフォルト値をオーバーライドします。

### 例

```python
# default_config.py にデフォルト値がある
DEFAULT_AZURE_API_KEY = "default-key-123"

# でも、ユーザーがこれを実行したら：
setx AZURE_OPENAI_API_KEY "user-key-456"

# アプリはユーザーのキーを使用する
```

---

## セキュリティに関する注意

⚠️ **重要な警告**

### ハードコード API キーのリスク

`default_config.py` に API キーをハードコードすると、以下のリスクがあります：

1. **ソースコード漏洩時の危険**
   - GitHub などにコミットした場合、API キーが公開される
   - 攻撃者が API キーを悪用できる

2. **EXE ファイルから抽出可能**
   - 逆アセンブリツールで API キーが抽出される可能性がある

### 推奨される方法

**推奨**: デフォルト値は設定したいが、API キーはハードコードしたくない場合：

```python
# default_config.py
DEFAULT_AZURE_API_KEY = ""  # 空のままにする
DEFAULT_AZURE_ENDPOINT = "https://your-resource.openai.azure.com"  # これは OK
DEFAULT_AZURE_DEPLOYMENT = "gpt-4-turbo"  # これは OK

# ユーザーは以下を実行:
setx AZURE_OPENAI_API_KEY "their-api-key"
```

この方法で：
- エンドポイントやデプロイメント名は EXE に埋め込める
- API キーはユーザーが環境変数で提供する
- ソースコードにはシークレットが含まれない

---

## テスト方法

### デフォルト設定が正しく適用されているか確認

```bash
# デバッグモードで実行（デフォルト設定の適用状況を表示）
python vibe_local_chat.py --debug
```

出力例：
```
[debug] Applied default configuration values
[debug]   - AZURE_OPENAI_ENDPOINT
[debug]   - AZURE_OPENAI_DEPLOYMENT
```

### default_config.py の設定を確認

```bash
# Python で直接実行
python default_config.py
```

出力例：
```
Current defaults configuration:
  Azure API Key: NOT SET
  Azure Endpoint: ***SET***
  Azure Deployment: gpt-4-turbo
  Azure API Version: 2024-08-01-preview

  Gemini API Key: NOT SET
  Gemini Model: gemini-2.0-flash
```

---

## よくある質問

### Q: デフォルト値を削除する方法は？

**A**: `default_config.py` を編集して、値を空の文字列に設定します：

```python
DEFAULT_AZURE_API_KEY = ""
DEFAULT_AZURE_ENDPOINT = ""
```

### Q: デフォルト値を変更したい場合は、再度 EXE をビルドする必要がありますか？

**A**: はい。デフォルト値は EXE ビルド時に固定されるため、値を変更する場合は再度ビルドが必要です。

### Q: ユーザーが環境変数を設定したら、デフォルト値は無視されますか？

**A**: はい。ユーザーが環境変数を設定すれば、デフォルト値はオーバーライドされます。

### Q: API キーをハードコードしても安全ですか？

**A**: いいえ。以下の理由から避けてください：
- ソースコード漏洩時のリスク
- EXE から逆アセンブリで抽出可能
- 定期的なキーローテーションが困難

---

## 実装例

### Azure OpenAI のデフォルト設定

```python
# default_config.py
DEFAULT_AZURE_API_KEY = ""  # ユーザーが設定する
DEFAULT_AZURE_ENDPOINT = "https://my-resource.openai.azure.com"
DEFAULT_AZURE_DEPLOYMENT = "gpt-4-turbo"
DEFAULT_AZURE_API_VERSION = "2024-08-01-preview"

DEFAULT_GEMINI_API_KEY = ""  # 未使用
DEFAULT_GEMINI_MODEL = "gemini-2.0-flash"
```

その後、ユーザーは以下を実行：

```powershell
setx AZURE_OPENAI_API_KEY "sk-abc123..."
```

### Gemini のデフォルト設定

```python
# default_config.py
DEFAULT_AZURE_API_KEY = ""
DEFAULT_AZURE_ENDPOINT = ""
DEFAULT_AZURE_DEPLOYMENT = ""
DEFAULT_AZURE_API_VERSION = ""

DEFAULT_GEMINI_API_KEY = ""  # ユーザーが設定する
DEFAULT_GEMINI_MODEL = "gemini-2.0-flash"
```

その後、ユーザーは以下を実行：

```powershell
setx GEMINI_API_KEY "your-gemini-key"
```

---

## バージョン

**バージョン**: 1.0.0
**最終更新**: 2026年2月27日
