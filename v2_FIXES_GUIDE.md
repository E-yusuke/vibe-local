# v2 修正ガイド - build_exe.bat エラー修正とデフォルト API キー設定

このドキュメントは、最近加えられた修正について説明しています。

## 修正内容

### 1. build_exe.bat エラー修正

**問題**: `build_exe.bat` 実行時に `"M" は、内部コマンドまたは外部コマンド...` というエラーが出ていました。

**原因**: バッチスクリプト内で遅延拡張変数の処理が不適切でした。

**修正内容**:
- `%variable%` の代わりに `!variable!` を使用（遅延拡張変数）
- `setlocal enabledelayedexpansion` で遅延拡張を有効化
- `endlocal` でスクリプト終了時にクリーンアップ

**修正ファイル**: `build_exe.bat`

**変更箇所**:
```batch
REM 修正前
echo ✓ Found: %PYTHON_VER%

REM 修正後
echo ✓ Found: !PYTHON_VER!
```

### 2. デフォルト API キー設定機能

**新機能**: EXE ビルド時に API キーやエンドポイントをデフォルト値として埋め込めるようにしました。

**利点**:
- ユーザーが API キーを設定しなくても、デフォルト値で自動起動
- エンドポイント、デプロイメント名などを事前設定可能
- ユーザーが環境変数を設定すれば、デフォルト値をオーバーライド可能

**新しいファイル**:
- `default_config.py` - デフォルト値を管理
- `DEFAULT_CONFIG_GUIDE.md` - デフォルト設定の使用方法

**修正ファイル**:
- `vibe_local_chat.py` - デフォルト設定の適用処理を追加

---

## 使い方

### build_exe.bat エラーの修正確認

```cmd
build_exe.bat
```

以下のような出力が表示されれば成功：

```
✓ Found: Python 3.11.0
✓ PyInstaller is available
✓ Dependencies installed
✓ Clean complete

Building EXE application...
This may take 1-2 minutes...

✓ Build complete!
✓ EXE created: dist\vibe-local.exe
```

### デフォルト API キー設定

#### ステップ 1: default_config.py を編集

```python
# default_config.py
DEFAULT_AZURE_API_KEY = ""  # ユーザーが設定するため空のままに
DEFAULT_AZURE_ENDPOINT = "https://your-resource.openai.azure.com"
DEFAULT_AZURE_DEPLOYMENT = "gpt-4-turbo"
DEFAULT_AZURE_API_VERSION = "2024-08-01-preview"
```

#### ステップ 2: build_exe.bat を実行

```cmd
build_exe.bat
```

#### ステップ 3: ユーザー向け配布

`create_distribution.bat` で配布パッケージを作成：

```cmd
create_distribution.bat
```

#### ステップ 4: ユーザーが API キーを設定

```powershell
setx AZURE_OPENAI_API_KEY "their-api-key"
```

#### ステップ 5: ユーザーが EXE を実行

```cmd
vibe-local.exe
```

---

## 実装詳細

### default_config.py の構成

```python
# API キーのデフォルト値
DEFAULT_AZURE_API_KEY = ""
DEFAULT_AZURE_ENDPOINT = ""
DEFAULT_AZURE_DEPLOYMENT = "gpt-4-turbo"
DEFAULT_AZURE_API_VERSION = "2024-08-01-preview"

DEFAULT_GEMINI_API_KEY = ""
DEFAULT_GEMINI_MODEL = "gemini-2.0-flash"

# デフォルト値を環境変数に適用
def apply_defaults():
    """優先順位: 環境変数 > デフォルト値"""
    if DEFAULT_AZURE_API_KEY and not os.environ.get("AZURE_OPENAI_API_KEY"):
        os.environ["AZURE_OPENAI_API_KEY"] = DEFAULT_AZURE_API_KEY
```

### vibe_local_chat.py での使用

```python
def main():
    """メイン処理"""
    # デフォルト設定を適用
    defaults_applied = apply_defaults()
    
    # 通常のコード処理...
```

### 優先順位

1. **ユーザーが設定した環境変数** ← 最優先
2. **default_config.py のデフォルト値**
3. **設定されていない** ← エラー

---

## セキュリティ上の注意

### ✅ 推奨される方法

```python
# default_config.py
DEFAULT_AZURE_API_KEY = ""  # 空のまま - ユーザーが設定
DEFAULT_AZURE_ENDPOINT = "https://..."  # OK - 公開情報
DEFAULT_AZURE_DEPLOYMENT = "gpt-4-turbo"  # OK - 公開情報
```

### ❌ 推奨されない方法

```python
# default_config.py
DEFAULT_AZURE_API_KEY = "sk-abc123xyz..."  # 危険 - 漏洩リスク
```

**理由**:
- ソースコード漏洩時に API キーが公開される
- EXE ファイルから逆アセンブリで抽出される可能性がある

---

## トラブルシューティング

### Q: build_exe.bat でまだエラーが出る

**A**: 以下を確認してください：
1. Python が PATH に含まれているか
   ```cmd
   python --version
   ```
2. PyInstaller がインストールされているか
   ```cmd
   pip install pyinstaller
   ```
3. CMD を管理者権限で実行しているか
4. `setlocal enabledelayedexpansion` で遅延拡張が有効か

### Q: デフォルト設定が反映されない

**A**: 以下を確認してください：
1. `default_config.py` に値が入っているか
   ```bash
   python default_config.py
   ```
2. 値が空でないか確認
   ```python
   DEFAULT_AZURE_ENDPOINT = "https://..."  # OK
   DEFAULT_AZURE_ENDPOINT = ""  # NG
   ```
3. EXE を再度ビルドしたか
   ```cmd
   build_exe.bat
   ```

### Q: ユーザーが環境変数を設定したのに、デフォルト値が使われている

**A**: これは正常な動作ではありません。以下を確認してください：
1. ユーザーがコマンドプロンプトを再起動したか（環境変数反映のため）
2. `setx` コマンドを使ったか（`set` は一時的）
3. デバッグモードで確認
   ```cmd
   vibe-local.exe --debug
   ```

---

## アップグレード手順

以前のバージョンから v2 へアップグレードする場合：

### 1. 新しいファイルを取得

```
new files:
  - default_config.py
  - DEFAULT_CONFIG_GUIDE.md
  - v2_FIXES_GUIDE.md (このファイル)

modified files:
  - build_exe.bat (バージョン 2.0)
  - vibe_local_chat.py (デフォルト設定対応)
```

### 2. 古い build_exe.bat をバックアップ

```cmd
ren build_exe.bat build_exe.bat.old
```

### 3. 新しいファイルを配置

新しい `build_exe.bat` と `vibe_local_chat.py` を置き換え

### 4. EXE を再度ビルド

```cmd
build_exe.bat
```

### 5. 配布パッケージを再作成

```cmd
create_distribution.bat
```

---

## 今後のバージョン改善予定

### v3 での予定

- [ ] ビルド時に環境変数から `default_config.py` を自動生成
- [ ] デフォルト設定の暗号化（API キーのセキュリティ向上）
- [ ] GUI での設定ウィザード
- [ ] マルチユーザー対応

---

## バージョン情報

**現在のバージョン**: 2.0
**最終更新日**: 2026年2月27日
**対応 OS**: Windows 10/11
**対応 Python**: 3.8+

---

## サポート

問題が発生した場合は、以下を確認してください：

1. `DEFAULT_CONFIG_GUIDE.md` - デフォルト設定の詳細ガイド
2. `BUILD_EXE_GUIDE.md` - EXE ビルドの完全ガイド
3. `SETUP_WINDOWS.md` - Windows セットアップガイド

それでも解決しない場合は、デバッグモードで詳細を確認：

```cmd
python vibe_local_chat.py --debug
```
