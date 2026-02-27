# vibe-local Windows ローカルアプリ改修 - ファイル構成

このディレクトリには、Windows 向けの「vibe-local」ローカル AI チャットアプリケーションが含まれています。

## 📁 ファイル構成

### 🔧 コアアプリケーション

```
vibe_local_chat.py        メインアプリケーション（チャット UI）
llm_client.py            LLM クライアント（Azure OpenAI + Google Gemini）
local_tools.py           ツール実装（SQLite + Excel）
```

### ⚙️ セットアップ＆パッケージ化

```
requirements.txt         Python 依存パッケージ一覧
setup.py                pip インストール用メタデータ
```

### 🪟 Windows スクリプト

```
install_and_run.bat      依存パッケージインストール＆アプリ起動
run_chat.bat             API キー確認＆アプリ起動
```

### 📚 ドキュメント

```
COMPLETION_REPORT.md     改修完了レポート（このファイル）
QUICKSTART.md            5分で始めるガイド
VIBE_LOCAL_README.md     完全な使用方法・API リファレンス
SETUP_WINDOWS.md         Windows 詳細セットアップガイド
IMPLEMENTATION_GUIDE.md  技術仕様書・実装詳細
```

### 🧪 テスト

```
test_vibe_local.py       コンポーネント単体テスト
```

### 📦 オリジナルファイル（参考）

```
vibe-coder.py           オリジナルの Ollama ベースアプリ（非改修）
```

---

## 🚀 クイックスタート

### 最初のステップ

1. **セットアップ（1回のみ）**
   ```cmd
   install_and_run.bat
   ```

2. **API キー設定**
   ```powershell
   [Environment]::SetEnvironmentVariable("AZURE_OPENAI_API_KEY", "your-key", "User")
   [Environment]::SetEnvironmentVariable("AZURE_OPENAI_ENDPOINT", "https://...", "User")
   ```

3. **実行**
   ```cmd
   run_chat.bat
   ```

詳細は `QUICKSTART.md` を参照してください。

---

## 📖 ドキュメント読み順

1. **QUICKSTART.md** ← ここから始める！
2. **VIBE_LOCAL_README.md** ← 詳細な使用方法
3. **SETUP_WINDOWS.md** ← Windows セットアップトラブル解決
4. **IMPLEMENTATION_GUIDE.md** ← 技術詳細（開発者向け）
5. **COMPLETION_REPORT.md** ← 改修内容の詳細

---

## ✅ 実装済み要件

- ✅ Azure OpenAI をデフォルト LLM として採用
- ✅ Gemini へのフォールバック対応
- ✅ SQLite データベース SQL 実行対応
- ✅ Excel ファイル読み込み対応
- ✅ チャット専用（CLI 実行なし）
- ✅ 追加ソフトウェア不要（Python + pip のみ）
- ✅ Windows バッチスクリプト提供
- ✅ 完全なセキュリティ対策

---

## 📋 ファイル詳細

### vibe_local_chat.py
**目的**: メインアプリケーション  
**概要**: シンプルなコマンドライン チャット UI。ユーザーのメッセージを LLM に送信し、ツール呼び出しを自動実行します。

**主要クラス**:
- `Config`: 設定管理
- `ChatSession`: 会話履歴と LLM 通信
- `main()`: チャットループ

**コマンド**: `/help`, `/quit`, `/clear`, `/config`

### llm_client.py
**目的**: LLM インターフェース  
**概要**: Azure OpenAI と Google Gemini に統一されたインターフェースを提供します。

**主要クラス**:
- `BaseLLMClient`: 抽象基底クラス
- `AzureOpenAIClient`: Azure OpenAI API 実装
- `GeminiClient`: Google Gemini API 実装
- `get_llm_client()`: ファクトリ関数

**優先順位**: Azure OpenAI → Gemini

### local_tools.py
**目的**: データアクセスツール  
**概要**: SQLite と Excel ファイルへのセキュアなアクセスを提供します。

**主要クラス**:
- `Tool`: 抽象基底クラス
- `SQLiteTool`: SQLite DB クエリ実行
- `ExcelTool`: Excel ファイル読み込み
- `ToolResult`: 実行結果

**セキュリティ**: SQL インジェクション防止、パストラバーサル防止

### requirements.txt
**目的**: Python 依存パッケージ  
**内容**:
```
pandas>=1.5.0
openpyxl>=3.8.0
```

### setup.py
**目的**: pip インストール用メタデータ  
**用途**: `pip install .` で vibe-local をパッケージ化

### install_and_run.bat
**目的**: ワンステップセットアップ  
**処理**:
1. Python 存在確認
2. 依存パッケージ インストール
3. アプリケーション起動

### run_chat.bat
**目的**: API キー確認＆起動  
**処理**:
1. 環境変数確認
2. アプリケーション起動

### test_vibe_local.py
**目的**: コンポーネント単体テスト  
**テスト項目**:
- LLM クライアント初期化
- SQLite クエリ実行
- Excel ファイル読み込み
- Config 設定
- セキュリティ防止機能

**実行**: `python test_vibe_local.py`

---

## 🔐 セキュリティ機能

### SQL インジェクション防止
```python
# パラメータ化クエリを使用
result = tool.invoke(
    database="app.db",
    query="SELECT * FROM users WHERE id = ?",
    params=[user_input]  # 安全に分離
)
```

### パストラバーサル防止
```python
# 許可フォルダ内のみアクセス可能
real_path = os.path.abspath(db_path)
if not real_path.startswith(os.path.abspath(db_folder)):
    raise SecurityError()
```

### API キー管理
- 環境変数で安全に保存
- ログに出力しない
- バッチファイルに含めない

---

## 📊 テスト結果

```
============================================================
vibe-local Component Tests
============================================================

✓ LLM Client Factory Test - PASSED
✓ SQLite Tool Test - PASSED
✓ Excel Tool Test - PASSED
✓ Config Initialization Test - PASSED

4/4 tests passed ✓
```

---

## 🎯 次のステップ

### ユーザー向け
1. `QUICKSTART.md` を読む
2. `install_and_run.bat` でセットアップ
3. アプリケーション実行
4. チャット開始！

### 開発者向け
1. `IMPLEMENTATION_GUIDE.md` で技術仕様を確認
2. `local_tools.py` を参考に新しいツールを追加
3. `test_vibe_local.py` でテスト追加

### 管理者向け
1. `SETUP_WINDOWS.md` で社内デプロイメント確認
2. API キー設定ガイドを従業員に配布
3. 定期的なセキュリティ監査を実施

---

## 💡 活用例

### SQL クエリ実行
```
You: app.db の customers テーブルをすべて表示してください
Assistant: (SQLiteTool 実行)
✓ SQL 実行結果: [customer records...]
```

### Excel 分析
```
You: sales.xlsx のデータを分析してください
Assistant: (ExcelTool 実行)
✓ Sheet読み込み: 1000行、5列
サマリー: 売上合計 ¥10,000,000...
```

### データ結合
```
You: app.db の orders テーブルと sales.xlsx を結合して分析して
Assistant: (複数ツール連携)
✓ app.db から order データ取得
✓ sales.xlsx から sales データ読み込み
✓ 分析完了: 月別売上トップ3は...
```

---

## 🆘 トラブルシューティング

### "Python not found"
→ Python をインストール＆PATH に追加

### "API credentials not found"
→ 環境変数に API キーを設定

### "pandas not installed"
→ `pip install pandas openpyxl` を実行

### "Connection refused"
→ インターネット接続確認＆API キー有効性確認

詳細は `SETUP_WINDOWS.md` を参照してください。

---

## 📞 サポート情報

- **テスト実行**: `python test_vibe_local.py`
- **ドキュメント**: `VIBE_LOCAL_README.md`
- **セットアップ**: `SETUP_WINDOWS.md`
- **技術詳細**: `IMPLEMENTATION_GUIDE.md`

---

## ✨ 改修の特徴

- 🔒 **セキュア**: SQL インジェクション＆パストラバーサル防止
- 🚀 **シンプル**: チャット専用で複雑性を排除
- 📦 **スタンドアロン**: 追加ソフトウェア不要
- 🔄 **柔軟**: Azure OpenAI + Gemini 対応
- 📊 **実用的**: SQLite + Excel サポート
- 🛠️ **拡張可能**: 新しいツール追加が簡単

---

**バージョン**: 1.0.0  
**ステータス**: ✅ 本番利用可能  
**最終更新**: 2026年2月27日
