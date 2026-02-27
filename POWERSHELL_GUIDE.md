# PowerShell スクリプト版ガイド

バッチファイル（.bat）の文字コード問題を回避するため、PowerShell スクリプト（.ps1）版を用意しました。

## 概要

| スクリプト | 説明 | 対応 |
|----------|------|------|
| `build_exe.bat` | EXE ビルド（バッチ版） | 文字コード問題あり（改善済み） |
| **`build_exe.ps1`** | **EXE ビルド（PowerShell 版）** | **✅ 推奨** |
| `create_distribution.bat` | 配布パッケージ作成（バッチ版） | 文字コード問題あり（改善済み） |
| **`create_distribution.ps1`** | **配布パッケージ作成（PowerShell 版）** | **✅ 推奨** |

## PowerShell 版の利点

✅ **文字コード問題なし** - Unicode をネイティブにサポート
✅ **カラー出力** - 成功/エラーを見やすい色で表示
✅ **より強力なエラーハンドリング** - 詳しいログ出力
✅ **Windows 10/11 に標準装備** - 追加インストール不要

## 使用方法

### ステップ 1: PowerShell を開く

**方法1: スタートメニューから**
1. スタートボタンをクリック
2. 「powershell」と入力
3. 「Windows PowerShell」をクリック

**方法2: キーボードショートカット**
- Windows キー + R → `powershell` → Enter

**方法3: 管理者権限で実行（推奨）**
1. スタートボタンをクリック
2. 「powershell」と入力
3. 「Windows PowerShell」を右クリック
4. 「管理者として実行」をクリック

### ステップ 2: スクリプトのあるディレクトリに移動

```powershell
cd C:\path\to\vibe-local
```

例：
```powershell
cd C:\Users\username\Desktop\vibe-local
```

### ステップ 3: EXE をビルド

```powershell
powershell -ExecutionPolicy Bypass -File build_exe.ps1
```

または（より簡潔）:
```powershell
.\build_exe.ps1
```

**実行ポリシーエラーが出た場合**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope CurrentUser
.\build_exe.ps1
```

### ステップ 4: 配布パッケージを作成

```powershell
.\create_distribution.ps1
```

### ステップ 5: 完了

`vibe-local-dist\` フォルダが生成されます。

---

## PowerShell スクリプトの特徴

### 色付き出力

```powershell
Write-Host "✓ Found: Python 3.11.0" -ForegroundColor Green
Write-Host "❌ Error: Python is not installed" -ForegroundColor Red
Write-Host "⚠️  Warning: PyInstaller not found" -ForegroundColor Yellow
```

実行時に以下のような色付き出力が表示されます：
- ✅ 成功 → 緑色
- ❌ エラー → 赤色
- ⚠️ 警告 → 黄色
- ℹ️ 情報 → シアン色

### より詳しいエラーメッセージ

バッチ版と異なり、PowerShell 版は以下のような詳しい情報を提供：

```powershell
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    # より詳しいエラー情報を表示可能
}
```

### Unicode 完全サポート

PowerShell は UTF-16LE をネイティブにサポートするため、以下の文字も完全に表示：

```
╔════════════════════════════════════════════════════════════════╗
║    vibe-local EXE Build Script (PowerShell)                   ║
╚════════════════════════════════════════════════════════════════╝
✓ ✗ ✅ ❌ ⚠️  📦 📋 💾 🚀 📝 🔧 etc.
```

---

## トラブルシューティング

### Q: 「このシステムでスクリプトの実行が無効になっているため...」というエラーが出る

**A**: 実行ポリシーを一時的に変更して実行：

```powershell
powershell -ExecutionPolicy Bypass -File build_exe.ps1
```

または永続的に変更（管理者権限必要）:

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope CurrentUser
```

### Q: PowerShell が見つからない

**A**: PowerShell は Windows 10/11 に標準装備です。

- スタートボタン → 「powershell」と入力
- または `Win + R` → `powershell` → OK

### Q: スクリプトが実行されない

**A**: 以下を確認：

1. PowerShell のバージョン確認
   ```powershell
   $PSVersionTable.PSVersion
   ```
   （PowerShell 3.0 以上推奨）

2. ファイルのエンコーディング確認
   - UTF-8 で保存されているか確認
   - テキストエディタで開き直して保存

3. PowerShell を管理者権限で実行

### Q: パスが見つからない

**A**: 正しいディレクトリに移動：

```powershell
# 現在のディレクトリ確認
Get-Location

# ファイルが存在するか確認
ls build_exe.ps1

# 正しいディレクトリに移動
cd C:\path\to\vibe-local
```

---

## バッチ版との比較

### バッチ版を使う場合

```cmd
build_exe.bat
```

**注意点**：
- `chcp 65001` で UTF-8 対応
- 文字コード問題が残る可能性
- シンプルで理解しやすい

### PowerShell 版を使う場合（推奨）

```powershell
.\build_exe.ps1
```

**利点**：
- 文字コード問題なし
- カラー出力で見やすい
- エラーハンドリング強力
- Windows 標準装備

---

## まとめ

| 項目 | バッチ版 | PowerShell 版 |
|------|---------|-------------|
| 文字コード | △ 改善済み | ✅ 完全対応 |
| 見やすさ | △ モノクロ | ✅ カラー |
| エラー情報 | △ 限定的 | ✅ 詳細 |
| 学習曲線 | ✅ 簡単 | △ やや複雑 |
| 推奨度 | △ | ✅ **推奨** |

---

**推奨**: PowerShell 版（`build_exe.ps1` と `create_distribution.ps1`）を使用してください。

バージョン: 1.0.0
最終更新: 2026年2月27日
