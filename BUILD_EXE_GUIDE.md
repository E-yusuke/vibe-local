# vibe-local EXE 化 - 完全ガイド

このドキュメントは、`vibe-local` チャットアプリケーションを Windows EXE として配布するための完全なガイドです。

## 概要

```
開発環境（このドキュメントがある環境）
  ↓
  vibe_local_chat.py + llm_client.py + local_tools.py
  ↓
  build_exe.bat を実行（PyInstaller）
  ↓
  dist\vibe-local.exe が生成
  ↓
  create_distribution.bat を実行
  ↓
  vibe-local-dist\ が生成（配布パッケージ）
  ↓
ユーザーに配布
```

## 環境要件（開発者向け）

### Windows 上で実施するもの

開発マシン（Windows）で以下を準備：

1. **Windows 10/11**
2. **Python 3.8 以上**
3. **必要なツール**:
   - PyInstaller
   - pandas, openpyxl

### インストール手順

```cmd
# Python 3.8+ をインストール（https://www.python.org）

# 作業ディレクトリに移動
cd C:\path\to\vibe-local

# 依存パッケージをインストール
pip install -r requirements.txt

# PyInstaller をインストール
pip install pyinstaller
```

## ステップバイステップガイド

### ステップ 1: ビルド環境の確認

```cmd
cd C:\path\to\vibe-local

# Python バージョン確認
python --version
# 出力例: Python 3.11.0

# PyInstaller 確認
pyinstaller --version
# 出力例: pyinstaller 6.x.x
```

### ステップ 2: EXE をビルド

```cmd
build_exe.bat
```

**実行内容**:
1. Python とツール確認
2. 依存パッケージのインストール確認
3. 前回のビルド成果物をクリーン
4. `dist\vibe-local.exe` をビルド

**出力例**:
```
╔════════════════════════════════════════════════════════════════╗
║    vibe-local EXE Build Script (Windows)                      ║
╚════════════════════════════════════════════════════════════════╝

✓ Found: Python 3.11.0
✓ PyInstaller is available
✓ Dependencies installed
✓ Clean complete

Building EXE application...
This may take 1-2 minutes...

✓ Build complete!

✓ EXE created: dist\vibe-local.exe
```

**ビルド時間**: 1-2 分

### ステップ 3: ビルド成果物の確認

```cmd
dir dist\
```

以下のようにファイルが生成されます：

```
dist\
└── vibe-local.exe          (100-150 MB)
```

### ステップ 4: テスト実行（オプション）

EXE がビルドされた環境で動作確認：

```cmd
cd dist
vibe-local.exe
```

**エラーが出た場合**:
- API キーが設定されていないはずなので、以下のエラーが表示されます：
  ```
  ❌ No LLM API credentials found.
  Please set ONE of the following:
  ```
- これは正常な動作です。API キーを設定すれば実行できます。

### ステップ 5: 配布パッケージの作成

```cmd
create_distribution.bat
```

**実行内容**:
1. `dist\vibe-local.exe` をコピー
2. `data\` フォルダを作成
3. `excel\` フォルダを作成
4. ドキュメントをコピー
5. セットアップスクリプトを生成

**出力例**:
```
╔════════════════════════════════════════════════════════════════╗
║   vibe-local Distribution Package Created Successfully!       ║
╚════════════════════════════════════════════════════════════════╝

📦 Package location: C:\path\to\vibe-local\vibe-local-dist\

📋 Folder structure:
   vibe-local-dist\
   ├── vibe-local.exe
   ├── data\
   ├── excel\
   ├── README.md
   ├── VIBE_LOCAL_README.md
   ├── SETUP_EXE.md
   └── setup_credentials.bat
```

### ステップ 6: 配布パッケージの確認

```cmd
tree vibe-local-dist /F
```

以下の構造が確認できます：

```
vibe-local-dist\
├── vibe-local.exe           (実行ファイル)
├── data\                    (SQLite ファイル用)
│   └── .gitkeep
├── excel\                   (Excel ファイル用)
│   └── .gitkeep
├── README.md                (ユーザーガイド)
├── README_EXE.md            (クイックスタート)
├── VIBE_LOCAL_README.md     (機能詳細)
├── SETUP_EXE.md             (このガイド)
└── setup_credentials.bat    (API キー設定ヘルパー)
```

### ステップ 7: ユーザーへ配布

`vibe-local-dist\` フォルダをユーザーに配布します。

**配布方法**:
- ZIP ファイルで圧縮して配布
- USB メモリで配布
- ネットワークドライブで配布
- etc.

## ユーザー向け：セットアップ手順

配布パッケージを受け取ったユーザーの実施内容：

### 1. パッケージを展開

```
vibe-local-dist\ をどこか任意の場所に展開
（例: C:\Users\username\Desktop\vibe-local）
```

### 2. API キーを設定

**方法1: セットアップスクリプトから（簡単）**

`setup_credentials.bat` をテキストエディタで開き、以下のコメント行をコメント解除して実行：

```batch
REM Option 1: Azure OpenAI
setx AZURE_OPENAI_API_KEY "your-api-key-here"
setx AZURE_OPENAI_ENDPOINT "https://your-resource.openai.azure.com"
setx AZURE_OPENAI_DEPLOYMENT "gpt-4-turbo"
```

**方法2: PowerShell から（推奨）**

PowerShell を管理者として開き、以下を実行：

```powershell
[Environment]::SetEnvironmentVariable("AZURE_OPENAI_API_KEY", "your-api-key", "User")
[Environment]::SetEnvironmentVariable("AZURE_OPENAI_ENDPOINT", "https://your-resource.openai.azure.com", "User")
[Environment]::SetEnvironmentVariable("AZURE_OPENAI_DEPLOYMENT", "gpt-4-turbo", "User")
```

### 3. PowerShell/CMD を再起動

**重要**: 環境変数を反映させるため、新しいターミナルウィンドウを開きます。

### 4. アプリを実行

```cmd
vibe-local.exe
```

または `vibe-local.exe` をダブルクリック

### 5. データを配置

SQLite や Excel ファイルを対応フォルダに配置：

```
vibe-local.exe が置かれている場所と同じ階層に:
  data\          ← .db ファイルをここに配置
  excel\         ← .xlsx ファイルをここに配置
```

## トラブルシューティング（開発者向け）

### ビルド失敗: "access denied"

```
ERROR: Cannot remove directory (Permission denied)
```

**原因**: antivirus やロックされたファイル

**解決方法**:
1. antivirus ソフトを一時的に無効化
2. `vibe-local.exe` が実行中でないか確認
3. CMD を管理者として実行

### ビルド失敗: "module not found"

```
ERROR: ModuleNotFoundError: No module named 'pandas'
```

**解決方法**:
```cmd
pip install -r requirements.txt
```

### ビルド失敗: "pyinstaller not found"

```
ERROR: 'pyinstaller' is not recognized
```

**解決方法**:
```cmd
pip install pyinstaller
python -m PyInstaller vibe_local.spec
```

### EXE が起動しない

**確認事項**:
1. ファイルが `dist\vibe-local.exe` に存在するか
2. 権限があるか
3. antivirus がブロックしていないか

**デバッグ方法**:
```cmd
cd dist
vibe-local.exe
```

コンソールに出力されるエラーメッセージを確認

### EXE サイズが大きい

```
vibe-local.exe が 200MB 以上ある場合
```

**解決方法**:
1. 不要なモジュールを `vibe_local.spec` の `excludedimports` に追加
2. UPX で圧縮（オプション）

## 高度なカスタマイズ

### vibe_local.spec の編集

PyInstaller 設定をカスタマイズする場合、`vibe_local.spec` を編集：

```python
# 例: アイコンを追加
icon='icon.ico'

# 例: バージョン情報を追加
version_file='version.txt'

# 例: 不要なモジュールを除外
excludedimports=[
    'matplotlib',
    'numpy',
    # 追加のモジュールをここに
]
```

修正後、再度ビルド：

```cmd
pyinstaller vibe_local.spec
```

### ワンフォルダ配布（onedir）

単一 EXE ではなく、複数ファイルで配布する場合：

`vibe_local.spec` で以下をコメント解除：

```python
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='vibe-local'
)
```

この場合、出力は `dist\vibe-local\` ディレクトリ構造になります。

## セキュリティに関する注意

### API キーをEXEに含めない

⚠️ **重要**: API キーを EXE に埋め込まないでください。

✅ **正しい方法**: ユーザーが環境変数で設定

❌ **間違った方法**: コード内に API キーを記述

### ハードコード厳禁

```python
# ❌ これはしない！
AZURE_OPENAI_API_KEY = "sk-xxx"

# ✅ これをする！
api_key = os.environ.get("AZURE_OPENAI_API_KEY")
```

## パフォーマンス最適化

### EXE サイズの削減

**デフォルト**: 100-150 MB

**削減方法**:

1. **不要なモジュールを除外**
   ```python
   # vibe_local.spec
   excludedimports=[
       'matplotlib',
       'numpy',
       'scipy',
       'sklearn',
   ]
   ```

2. **UPX で圧縮**（オプション）
   ```cmd
   pip install upx
   upx --best -o vibe-local-small.exe vibe-local.exe
   ```
   結果: 30-50 MB に削減（ただし解凍に時間がかかる）

## 配布チェックリスト

配布前に以下を確認してください：

- [ ] `build_exe.bat` で EXE ビルド成功
- [ ] `dist\vibe-local.exe` が存在
- [ ] `create_distribution.bat` で配布パッケージ生成成功
- [ ] `vibe-local-dist\` フォルダに以下が含まれている：
  - [ ] `vibe-local.exe`
  - [ ] `data\` フォルダ
  - [ ] `excel\` フォルダ
  - [ ] `README.md`
  - [ ] `README_EXE.md`
  - [ ] `SETUP_EXE.md`
  - [ ] `setup_credentials.bat`
- [ ] テストマシンで EXE が実行可能（API キー設定後）
- [ ] ドキュメントに誤りがないか確認
- [ ] LICENSE ファイルが含まれている
- [ ] README が最新の情報を反映している

## 総括

```
Windows 開発マシンで:

1. build_exe.bat        → EXE をビルド
   ↓
2. create_distribution.bat → 配布パッケージを作成
   ↓
3. vibe-local-dist\ をユーザーに配布
   ↓

ユーザーは:

1. パッケージを展開
2. API キーを設定（環境変数）
3. vibe-local.exe を実行
4. チャット開始
```

---

**重要なポイント**:

✅ Windows 環境で実施すること
✅ API キーは環境変数で設定させること
✅ data\ と excel\ は EXE と同じ階層に配置させること
✅ ドキュメントをしっかり整備すること

---

**バージョン**: 1.0.0
**最終更新**: 2026年2月27日
**対応 OS**: Windows 10/11
**対応 Python**: 3.8+
