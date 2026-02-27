# Windows セットアップガイド

## 前提条件

- Windows 10/11 以上
- インターネット接続
- 管理者権限（初回セットアップ時のみ必要な場合あり）

## ステップ 1: Python のインストール

1. [python.org](https://www.python.org/downloads/) から Python 3.9 以上をダウンロード
2. インストーラーを実行
3. **重要**: 「Add Python to PATH」にチェックを入れる
4. 「Install Now」をクリック

## ステップ 2: vibe-local のセットアップ

### Option A: バッチスクリプトを使用（推奨）

1. vibe-local フォルダを展開
2. `install_and_run.bat` をダブルクリック
3. プロンプトに従って進める

### Option B: コマンドプロンプトで手動セットアップ

```cmd
# vibe-local フォルダに移動
cd C:\path\to\vibe-local

# 依存パッケージをインストール
pip install -r requirements.txt
```

## ステップ 3: API 認証情報の設定

### Option A: Azure OpenAI を使用する場合

#### 方法 1: PowerShell でセットアップ（永続化）

```powershell
# PowerShell を管理者として実行
$key = "your-azure-openai-api-key-here"
$endpoint = "https://your-resource-name.openai.azure.com"
$deployment = "gpt-4-turbo"

[Environment]::SetEnvironmentVariable("AZURE_OPENAI_API_KEY", $key, "User")
[Environment]::SetEnvironmentVariable("AZURE_OPENAI_ENDPOINT", $endpoint, "User")
[Environment]::SetEnvironmentVariable("AZURE_OPENAI_DEPLOYMENT", $deployment, "User")
[Environment]::SetEnvironmentVariable("AZURE_OPENAI_API_VERSION", "2024-08-01-preview", "User")

Write-Host "環境変数を設定しました。PowerShell を再起動してください。"
```

#### 方法 2: バッチファイルでセットアップ（自動）

`setup_azure.bat` を作成：

```batch
@echo off
setx AZURE_OPENAI_API_KEY "your-api-key-here"
setx AZURE_OPENAI_ENDPOINT "https://your-resource.openai.azure.com"
setx AZURE_OPENAI_DEPLOYMENT "gpt-4-turbo"
setx AZURE_OPENAI_API_VERSION "2024-08-01-preview"
echo Environment variables set. Please restart your terminal.
pause
```

実行：
```cmd
setup_azure.bat
```

#### 方法 3: システム環境変数設定（GUI）

1. Windows 起動メニューで「環境変数」を検索
2. 「システム環境変数を編集」をクリック
3. 「環境変数」ボタンをクリック
4. 「新規」をクリックして以下を追加：

| 変数名 | 値 |
|--------|-----|
| `AZURE_OPENAI_API_KEY` | `your-api-key-here` |
| `AZURE_OPENAI_ENDPOINT` | `https://your-resource.openai.azure.com` |
| `AZURE_OPENAI_DEPLOYMENT` | `gpt-4-turbo` |
| `AZURE_OPENAI_API_VERSION` | `2024-08-01-preview` |

5. OK をクリックして保存
6. コマンドプロンプト・PowerShell を再起動

### Option B: Google Gemini を使用する場合

```powershell
# PowerShell での設定
$key = "your-gemini-api-key-here"
[Environment]::SetEnvironmentVariable("GEMINI_API_KEY", $key, "User")
[Environment]::SetEnvironmentVariable("GEMINI_MODEL", "gemini-2.0-flash", "User")
```

## ステップ 4: データフォルダの確認

アプリ実行時に自動作成されるフォルダ：

```
%LOCALAPPDATA%\vibe-local\
├── data\              # SQLite ファイル置き場
└── excel\             # Excel ファイル置き場
```

手動作成する場合：

```cmd
mkdir "%LOCALAPPDATA%\vibe-local\data"
mkdir "%LOCALAPPDATA%\vibe-local\excel"
```

Explorer で確認：
- キーボードショートカット: `Win + R`
- `%LOCALAPPDATA%\vibe-local` を入力
- Enter キー

## ステップ 5: アプリケーションの起動

### 方法 1: バッチファイル（推奨）

```cmd
run_chat.bat
```

### 方法 2: コマンドプロンプトから

```cmd
cd C:\path\to\vibe-local
python vibe_local_chat.py
```

### 方法 3: ショートカット作成

1. `run_chat.bat` を右クリック → 送信 → デスクトップ（ショートカット作成）
2. 作成したショートカットをダブルクリックして実行
3. デスクトップの「run_chat」ショートカットからいつでも起動可能

## Azure OpenAI の認証情報取得方法

1. [Azure Portal](https://portal.azure.com/) にログイン
2. リソース グループ内で OpenAI リソースを探す
3. 「キーとエンドポイント」セクションで：
   - API キー（Key 1 または Key 2）をコピー
   - エンドポイント URL をコピー
   - 使用デプロイメント名を確認

## Google Gemini の認証情報取得方法

1. [Google AI Studio](https://aistudio.google.com/) にアクセス
2. 「Get API Key」をクリック
3. 新しいプロジェクトを作成またはプロジェクトを選択
4. API キーを生成
5. キーをコピーして環境変数に設定

## トラブルシューティング

### "Python が見つかりません" エラー

```cmd
# PowerShell で確認
python --version
```

解決方法:
- Python を再インストール（「Add to PATH」にチェック）
- コマンドプロンプト/PowerShell を再起動

### "モジュールが見つかりません" エラー

```cmd
# pandas/openpyxl のインストール
pip install pandas openpyxl

# または全依存関係をリセット
pip install --upgrade -r requirements.txt
```

### "API credentials not found" エラー

```cmd
# 環境変数が設定されているか確認
echo %AZURE_OPENAI_API_KEY%

# または
echo %GEMINI_API_KEY%
```

何も表示されない場合は、ステップ 3 でセットアップを実行してください。

### API キーが無効なエラー

1. API キーを再度確認
2. スペースや特殊文字がないか確認
3. キーが有効期限内か確認
4. コマンドプロンプト/PowerShell を再起動して再試行

### SQLite ファイルが見つからないエラー

```cmd
# vibe-local データフォルダを開く
explorer "%LOCALAPPDATA%\vibe-local\data\"

# ファイルが存在するか確認
dir "%LOCALAPPDATA%\vibe-local\data\"
```

### Excel ファイルが読めないエラー

```cmd
# vibe-local Excel フォルダを開く
explorer "%LOCALAPPDATA%\vibe-local\excel\"

# ファイルが .xlsx 形式か確認
# .xls 形式の場合は .xlsx に変換
```

## アンインストール

### 完全アンインストール

```cmd
# 依存パッケージの削除
pip uninstall pandas openpyxl

# または環境変数を削除（GUI）
# システム環境変数から AZURE_OPENAI_* または GEMINI_* を削除

# vibe-local フォルダを削除
rmdir /s "C:\path\to\vibe-local"
```

### データの保持

データフォルダは手動で削除:
```cmd
explorer "%LOCALAPPDATA%\vibe-local\"
```

## よくある質問

### Q: 複数の LLM API キーを設定できますか？

A: 優先順位は以下の通りです：
1. Azure OpenAI（AZURE_OPENAI_API_KEY 設定時）
2. Google Gemini（GEMINI_API_KEY 設定時）

どちらか一方のみ有効な状態にしてください。

### Q: ローカルネットワークでのみ使用できますか？

A: Azure OpenAI と Gemini はクラウドサービスなため、インターネット接続が必須です。オンプレミスのみの環境では使用できません。

### Q: パスワードをバッチファイルに書き込んでも安全ですか？

A: セキュリティ上、環境変数をシステム環境として保存することをお勧めします。バッチファイルにハードコードしないでください。

### Q:複数のコンピューターで設定を同期できますか？

A: 各コンピューターで個別に環境変数を設定してください。

## サポートとドキュメント

- `VIBE_LOCAL_README.md` - アプリケーション使用方法
- `--help` - コマンドラインヘルプ
- `/help` - アプリ内ヘルプ
