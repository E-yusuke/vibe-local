# vibe-local クイックスタート

## 5分で始める

### 1. Python をインストール

[python.org](https://www.python.org/) から Python 3.9+ をダウンロード・インストール

**重要**: セットアップ時に「Add Python to PATH」にチェック ✓

### 2. vibe-local をセットアップ

```cmd
cd C:\path\to\vibe-local
python -m pip install -r requirements.txt
```

### 3. API キーを設定

#### Azure OpenAI の場合（推奨）

PowerShell を開いて：

```powershell
[Environment]::SetEnvironmentVariable("AZURE_OPENAI_API_KEY", "your-key", "User")
[Environment]::SetEnvironmentVariable("AZURE_OPENAI_ENDPOINT", "https://your-resource.openai.azure.com", "User")
[Environment]::SetEnvironmentVariable("AZURE_OPENAI_DEPLOYMENT", "gpt-4-turbo", "User")
```

#### Google Gemini の場合

```powershell
[Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "your-key", "User")
```

### 4. アプリを起動

```cmd
python vibe_local_chat.py
```

または

```cmd
run_chat.bat
```

## 次のステップ

- `/help` でコマンド一覧を表示
- `app.db の users テーブルを表示して` など、チャットで指示
- `data.xlsx を分析して` など、Excel ファイルを操作

## よくある初期エラー

| エラー | 対応 |
|--------|------|
| "No module named pandas" | `pip install pandas openpyxl` |
| "API credentials not found" | Azure/Gemini キーを環境変数に設定 |
| "Connection refused" | インターネット接続を確認 |

## API キーの取得

### Azure OpenAI

1. [Azure Portal](https://portal.azure.com/) にログイン
2. OpenAI リソースを検索
3. 「キーとエンドポイント」から KEY 1 と Endpoint URL をコピー

### Google Gemini

1. [Google AI Studio](https://aistudio.google.com/) にアクセス
2. 「Get API Key」をクリック
3. API キーをコピー

## データの場所

```
%LOCALAPPDATA%\vibe-local\
├── data\        ← SQLite ファイルをここに置く
└── excel\       ← Excel ファイルをここに置く
```

Explorer で開く:
```cmd
explorer %LOCALAPPDATA%\vibe-local
```

## テスト

```cmd
python test_vibe_local.py
```

すべてのテストが「PASSED」ならセットアップ完了です！

## ドキュメント

- `VIBE_LOCAL_README.md` - 詳細な使用方法
- `SETUP_WINDOWS.md` - Windows セットアップ詳細
- `IMPLEMENTATION_GUIDE.md` - 技術仕様書

## サポート

問題が発生した場合：

1. `python test_vibe_local.py` でテスト実行
2. API キーが正しく設定されているか確認
3. インターネット接続を確認
4. Python 3.8+ が インストール済みか確認

---

**楽しいチャティングを！🚀**
