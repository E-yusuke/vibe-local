# vibe-local - AI チャットアプリケーション

Windows 向けスタンドアロン EXE アプリケーションです。Python をインストール不要で、すぐに使用できます。

## 特徴

- 🤖 **Azure OpenAI & Gemini 対応**: 高速で信頼性の高い LLM を使用
- 💾 **SQLite 対応**: データベースをチャットで操作
- 📊 **Excel 対応**: Excel ファイルをチャットで分析
- 🔒 **セキュア**: CLI 実行なし、データアクセスのみ
- 📦 **スタンドアロン**: Python 不要、EXE だけで実行可能

## クイックスタート

### 1. API キーを設定

PowerShell（管理者）で以下を実行：

**Azure OpenAI の場合（推奨）:**
```powershell
[Environment]::SetEnvironmentVariable("AZURE_OPENAI_API_KEY", "your-api-key", "User")
[Environment]::SetEnvironmentVariable("AZURE_OPENAI_ENDPOINT", "https://your-resource.openai.azure.com", "User")
[Environment]::SetEnvironmentVariable("AZURE_OPENAI_DEPLOYMENT", "gpt-4-turbo", "User")
```

**Google Gemini の場合:**
```powershell
[Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "your-api-key", "User")
```

### 2. PowerShell/CMD を再起動

新しいターミナルウィンドウで環境変数が反映されます。

### 3. アプリを実行

`vibe-local.exe` をダブルクリック、または

```cmd
vibe-local.exe
```

## データの配置

### SQLite データベース

EXE と同じフォルダに `data\` フォルダを作成し、`.db` ファイルを配置：

```
vibe-local.exe
data\
├── app.db
├── users.db
└── ...
```

### Excel ファイル

EXE と同じフォルダに `excel\` フォルダを作成し、`.xlsx` ファイルを配置：

```
vibe-local.exe
excel\
├── data.xlsx
├── sales.xlsx
└── ...
```

## 使用例

```
You: app.db の users テーブルをすべて表示して
Assistant: (SQLite クエリ実行)
✓ sqlite_query:
[
  {
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com"
  },
  ...
]

You: sales.xlsx の概要を教えてください
Assistant: (Excel ファイル分析)
✓ read_excel: Sheet1 - 5列、1000行
売上合計: ¥10,000,000
...
```

## コマンド

チャット中に使用可能なコマンド：

```
/help       - ヘルプを表示
/quit       - アプリを終了
/exit       - アプリを終了
/clear      - 会話履歴をクリア
/config     - 現在の設定を表示
```

## トラブルシューティング

### "API credentials not found" エラー

```
❌ No LLM API credentials found.
```

**原因**: 環境変数が設定されていない

**解決方法**:
1. PowerShell で環境変数を設定（上記参照）
2. PowerShell/CMD を完全に再起動
3. 環境変数を確認：
   ```cmd
   echo %AZURE_OPENAI_API_KEY%
   ```

### "data folder not found" エラー

**解決方法**:
1. EXE と同じフォルダに `data\` フォルダを作成
2. `excel\` フォルダも作成

```cmd
mkdir data
mkdir excel
```

### ファイルが見つからない

**SQLite の場合**:
- ファイルが `data\` フォルダに存在するか確認
- ファイル拡張子が `.db` か確認

**Excel の場合**:
- ファイルが `excel\` フォルダに存在するか確認
- ファイル形式が `.xlsx` か確認（`.xls` は非対応）

### API キーが無効

**解決方法**:
1. API キーを再度確認（スペースやコピーミスがないか）
2. API キーが有効期限内か確認
3. インターネット接続を確認
4. Azure/Gemini サービスが正常に動作しているか確認

## FAQ

**Q: Python をインストールする必要がありますか？**
→ いいえ。EXE にすべて含まれています。

**Q: データはどこに保存されますか？**
→ `data\` と `excel\` フォルダに保存されます（EXE と同じ場所）。

**Q: オフラインで使用できますか？**
→ いいえ。Azure OpenAI/Gemini API の呼び出しにインターネット接続が必須です。

**Q: データベースサイズに制限はありますか？**
→ SQLite は理論上無制限、Excel は pandas の制限に準拠（通常 GB 単位まで可）。

**Q: 複数の SQLite ファイルを同時に使用できますか？**
→ はい。`data\` フォルダに複数の `.db` ファイルを配置できます。

## ドキュメント

詳細情報は以下を参照してください：

- `VIBE_LOCAL_README.md` - 完全な機能説明
- `SETUP_EXE.md` - EXE ビルドと配布ガイド

## サポート

問題が発生した場合：

1. 環境変数が正しく設定されているか確認
2. インターネット接続を確認
3. API キーの有効性を確認
4. ファイルパスを確認（EXE と同じフォルダに `data\`, `excel\`)

## ライセンス

MIT License

---

**楽しいチャティングを！🚀**
