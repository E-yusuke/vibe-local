# vibe-local EXE アプリケーション - ビルド＆配布ガイド

このドキュメントは、`vibe-local` を Windows EXE アプリケーションとしてビルドし、配布するための手順です。

## 概要

EXE化により以下が実現されます：

- 🎁 **ユーザーは Python をインストール不要**
- 📦 **単一の EXE ファイルで配布**
- 📁 **EXE と同階層に `data`、`excel` フォルダを配置**
- 💾 **データベースと Excel ファイルを簡単に管理**

## ビルド環境（開発者向け）

### 前提条件

- Windows 10/11
- Python 3.8 以上
- インターネット接続

### ステップ 1: 開発環境の準備

```cmd
cd C:\path\to\vibe-local

# 依存パッケージをインストール
pip install -r requirements.txt

# PyInstaller をインストール
pip install pyinstaller
```

### ステップ 2: EXE をビルド

```cmd
build_exe.bat
```

このスクリプトが自動的に以下を実行します：

1. Python とツールの確認
2. 依存パッケージのインストール
3. 前回のビルド成果物をクリーン
4. EXE をビルド（`dist\vibe-local.exe` に生成）

**ビルド時間**: 1-2 分

### ステップ 3: ビルド成果物の確認

```
dist\
└── vibe-local.exe          (約 100-150 MB)
```

## 配布パッケージの作成

### フォルダ構成

ユーザーに配布する際は、以下の構造にします：

```
vibe-local\                 ← 配布用ルートフォルダ
├── vibe-local.exe          ← メインアプリケーション
├── data\                   ← SQLite ファイル保存先
│   ├── .gitkeep            (または別のマーカーファイル)
│   └── (ユーザーが SQLite ファイルを配置)
├── excel\                  ← Excel ファイル保存先
│   ├── .gitkeep            (または別のマーカーファイル)
│   └── (ユーザーが Excel ファイルを配置)
├── README.md               ← ユーザー用ドキュメント
├── SETUP_EXE.md            ← このドキュメント
├── sample_data.db          ← (オプション) サンプル DB
└── sample_data.xlsx        ← (オプション) サンプル Excel
```

### 自動スクリプト：配布パッケージの作成

以下のスクリプトで配布パッケージを自動作成できます：

**create_distribution.bat** を実行：

```cmd
create_distribution.bat
```

このスクリプトは以下を実行します：

1. `dist\vibe-local.exe` をコピー
2. `data\` フォルダを作成
3. `excel\` フォルダを作成
4. `README.md` と `SETUP_EXE.md` をコピー
5. `vibe-local-dist\` 配布パッケージを生成

## ユーザー向け：アプリケーション実行方法

### 初回セットアップ

1. **配布パッケージを解凍**
   ```
   vibe-local-dist\
   ├── vibe-local.exe
   ├── data\
   ├── excel\
   └── README.md
   ```

2. **API 認証情報を設定**
   
   PowerShell（管理者）で実行：
   ```powershell
   # Azure OpenAI の場合
   [Environment]::SetEnvironmentVariable("AZURE_OPENAI_API_KEY", "your-api-key", "User")
   [Environment]::SetEnvironmentVariable("AZURE_OPENAI_ENDPOINT", "https://your-resource.openai.azure.com", "User")
   [Environment]::SetEnvironmentVariable("AZURE_OPENAI_DEPLOYMENT", "gpt-4-turbo", "User")
   ```

   または Gemini の場合：
   ```powershell
   [Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "your-api-key", "User")
   ```

3. **PowerShell/CMD を再起動**（環境変数を反映させるため）

### アプリケーション実行

方法1: **EXE をダブルクリック**
```
vibe-local.exe をダブルクリック → チャット開始
```

方法2: **コマンドプロンプト/PowerShell から実行**
```cmd
vibe-local.exe
```

方法3: **コマンドラインオプション付きで実行**
```cmd
vibe-local.exe --debug
vibe-local.exe --temp 0.5
```

### データの配置

**SQLite ファイルの配置**
```
vibe-local\data\
├── app.db
├── users.db
└── ...
```

EXE と同じフォルダの `data\` 以下に SQLite ファイルを配置します。

**Excel ファイルの配置**
```
vibe-local\excel\
├── data.xlsx
├── analysis.xlsx
└── ...
```

EXE と同じフォルダの `excel\` 以下に `.xlsx` ファイルを配置します。

### チャット例

```
You: app.db の users テーブルを表示して
Assistant: (SQLiteTool が実行)
✓ sqlite_query:
[{"id": 1, "name": "Alice", ...}, ...]

You: data.xlsx を分析して
Assistant: (ExcelTool が実行)
✓ read_excel:
データを読み込みました...
```

## EXE ファイルサイズの最適化

デフォルトでは、EXE は 100-150 MB 程度になります（Python ランタイムを含むため）。

### サイズ削減方法

#### 方法1: UPX で圧縮（オプション）

[UPX](https://upx.github.io/) をインストール後、手動で EXE を圧縮：

```cmd
upx --best -o vibe-local-compressed.exe vibe-local.exe
```

結果: 約 30-50 MB に削減

#### 方法2: `spec` ファイルを修正

`vibe_local.spec` で不要なモジュールを除外：

```python
excludedimports=[
    'matplotlib',
    'numpy',
    'scipy',
    'sklearn',
    'IPython',
    # さらに必要に応じて追加
],
```

### ワンフォルダ配布版（onedir）

単一 EXE ではなく、複数ファイルで配布する場合：

`vibe_local.spec` で `COLLECT` 部分をコメント解除して再ビルド。

## トラブルシューティング

### "Python not found" エラー

```
❌ Error: Python is not installed or not in PATH
```

**解決方法**:
1. Python をインストール
2. インストール時に「Add Python to PATH」にチェック
3. コマンドプロンプト/PowerShell を再起動

### "PyInstaller not found" エラー

```
pyinstaller: not found
```

**解決方法**:
```cmd
pip install pyinstaller
```

### ビルド中に "access denied" エラー

```
ERROR: Cannot remove directory (Permission denied)
```

**解決方法**:
1. antivirus ソフトが干渉していないか確認
2. EXE が実行中でないか確認
3. CMD を管理者として実行

### EXE 実行時に "API credentials not found" エラー

```
❌ No LLM API credentials found.
```

**解決方法**:
1. 環境変数が正しく設定されているか確認：
   ```cmd
   echo %AZURE_OPENAI_API_KEY%
   ```
2. PowerShell/CMD を再起動して環境変数を反映

### EXE 実行時に "data folder not found" エラー

```
❌ No such directory: data
```

**解決方法**:
1. EXE と同じフォルダに `data\` フォルダが存在するか確認
2. 存在しない場合は手動作成：
   ```cmd
   mkdir data
   mkdir excel
   ```

## 配布時の注意事項

### セキュリティ

- **API キーを含めない**: EXE には API キーを埋め込まない
- **ユーザーが環境変数で設定**: 各ユーザーが自分の API キーを設定
- **HTTPs のみ**: API 呼び出しは必ず HTTPS

### ライセンス

- MIT ライセンスを明記
- LICENSE ファイルを配布パッケージに含める

### ドキュメント

- README.md を配布パッケージに含める
- セットアップ手順を記載
- トラブルシューティング情報を含める

## 参考：PyInstaller の詳細オプション

### 再ビルド

```cmd
REM dist\ と build\ をクリーンアップしてから再ビルド
rmdir /s /q dist
rmdir /s /q build
pyinstaller vibe_local.spec
```

### デバッグ情報付きビルド

`vibe_local.spec` で `debug=True` に変更してビルド：

```python
exe = EXE(
    # ...
    debug=True,  # デバッグ情報を含める
    # ...
)
```

### バージョン情報の追加

Windows EXE にバージョン情報を添付することもできます（別途手順が必要）。

## よくある質問

**Q: EXE が実行されない（起動しない）**
→ `CMD.exe` を管理者として開き、EXE パスを指定して実行し、エラーメッセージを確認してください。

**Q: API キーはどこに保存されますか？**
→ EXE には保存されません。Windows 環境変数に保存されます。

**Q: オフラインで実行できますか？**
→ いいえ。Azure OpenAI/Gemini API 呼び出しにインターネット接続が必須です。

**Q: データベースファイルはどこに保存されますか？**
→ EXE と同じフォルダの `data\` フォルダに自動保存されます。

**Q: EXE をアップデートするには？**
→ 新しい EXE をビルドして、古い EXE を置き換えます。`data\` と `excel\` フォルダはそのままです。

## まとめ

```
開発者の作業:
1. build_exe.bat を実行
2. dist\vibe-local.exe を確認
3. create_distribution.bat で配布パッケージ作成
4. ユーザーに配布

ユーザーの作業:
1. パッケージを解凍
2. API キーを環境変数で設定
3. vibe-local.exe をダブルクリック
4. チャット開始
```

---

**最終確認チェックリスト**

- [ ] build_exe.bat で EXE ビルド成功
- [ ] dist\vibe-local.exe が生成されている
- [ ] create_distribution.bat で配布パッケージ作成
- [ ] vibe-local-dist\ フォルダに data\ と excel\ が含まれている
- [ ] README.md と SETUP_EXE.md が配布パッケージに含まれている
- [ ] テストユーザーで EXE が実行できることを確認

---

**バージョン**: 1.0.0
**最終更新**: 2026年2月27日
