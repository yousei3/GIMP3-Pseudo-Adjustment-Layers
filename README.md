# Pseudo Adjustment Layer for GIMP 3

-----

## English

**Pseudo Adjustment Layer** is a Python plugin for GIMP 3.0 / 3.2 that simulates the classic "Adjustment Layer" workflow found in other photo editing software by leveraging GIMP 3's new Non-Destructive Editing (NDE) features.

### ✨ Features

  * **One-Click NDE Groups**: Automatically creates a Layer Group, adds a transparent Dummy Layer, applies your active selection as a Layer Mask, and attaches the selected GEGL/GIMP filter as a non-destructive effect.
  * **Familiar Palette UI**: The filter list is categorized exactly like the official GIMP menu (Colors, Blur, Enhance, etc.), complete with submenus and visual icons.
  * **Workflow Tools**:
      * 🔍 Real-time Search.
      * ⭐ Favorites & 📝 History (Right-click any filter to add/remove).
      * 🌚 Hide unused filters (They move to the 📦 Hidden folder).
  * **Third-Party Plugin Support**: Automatically detects installed custom GEGL filters (such as LinuxBeaver's `lb:` plugins) and neatly organizes them into a 🧩 **Others** folder.
  * **Built-in Translation**: Generates local JSON files to seamlessly translate filter names into your preferred language without touching the code.

### 📥 Installation

1.  Download `pseudo_adjustment_layers.py`.
2.  Place the file into your **User** GIMP plug-ins folder:
      * **Windows:** `%APPDATA%\GIMP\3.0\plug-ins\`
      * **Linux:** `~/.config/GIMP/3.0/plug-ins/`
      * **macOS:** `~/Library/Application Support/GIMP/3.0/plug-ins/`
3.  *(Linux/macOS only)* Make the file executable (`chmod +x pseudo_adjustment_layers.py`).
4.  Restart GIMP.

> ⚠️ **IMPORTANT WARNING FOR WINDOWS USERS:**
> Do **NOT** place this plugin in the system directory (e.g., `C:\Program Files\GIMP 3\...\plug-ins\`). The plugin needs write permissions to save your Favorites, History, and Language JSON files. Placing it in a system folder will cause permission errors.

### 🚀 How to Use

1.  Open an image in GIMP.
2.  Go to **Image \> Filters \> Pseudo Adjustment Layer**.
3.  **[FIRST RUN ONLY]** Click the **`🔄 Reset List`** button at the bottom of the palette. This scans your GIMP installation for all available filters, validates them, and builds the menu.
4.  Select or double-click a filter to apply it as an adjustment layer.

### ⚙️ Requirements

  * GIMP 3.0.0-RC1 or newer.
  * Python 3 support enabled in GIMP.

### 📄 License

GPLv3

-----

## 日本語

**Pseudo Adjustment Layer** は、GIMP 3 の新しい非破壊編集（NDE）機能を活用し、他の画像編集ソフトでおなじみの「調整レイヤー」のワークフローを再現する GIMP 3.0 / 3.2 向け Python プラグインです。

### ✨ 主な機能

  * **ワンクリックでNDEグループ作成**: 選択範囲をレイヤーマスクに変換し、透明なダミーレイヤーを内包した「レイヤーグループ」を自動作成。指定したフィルタを非破壊エフェクトとしてグループに適用します。
  * **直感的なパレットUI**: GIMP公式メニュー（色、ぼかし、強調など）の階層構造を完全に再現。折りたたみ可能なサブメニューとアイコンで視覚的にわかりやすく整理されています。
  * **ワークフロー支援**:
      * 🔍 リアルタイム検索機能
      * ⭐ お気に入り ＆ 📝 履歴機能（右クリックで追加/解除）
      * 🌚 使わないフィルタの非表示機能（📦 Hiddenフォルダに移動します）
  * **サードパーティ製プラグイン対応**: LinuxBeaver氏のプラグインなど、公式メニューにない外部GEGLフィルタを自動検出し、🧩 **Others（その他）** フォルダに自動格納します。
  * **自動翻訳システム**: GIMP内蔵の翻訳データを利用して各言語のJSONファイルを自動生成。コードを編集することなく、UIをお好みの言語に切り替え可能です。

### 📥 インストール方法

1.  `pseudo_adjustment_layers.py` をダウンロードします。
2.  OSの **ユーザー専用** のGIMPプラグインフォルダに配置します：
      * **Windows:** `%APPDATA%\GIMP\3.0\plug-ins\`
      * **Linux:** `~/.config/GIMP/3.0/plug-ins/`
      * **macOS:** `~/Library/Application Support/GIMP/3.0/plug-ins/`
3.  *(Linux/macOS のみ)* ファイルに実行権限を付与します（`chmod +x pseudo_adjustment_layers.py`）。
4.  GIMPを再起動します。

> ⚠️ **Windowsユーザーへの重要なお願い：**
> プラグインをシステムフォルダ（例: `C:\Program Files\GIMP 3\...\plug-ins\`）には **絶対に配置しないでください**。お気に入りや履歴のJSONファイルを保存できず、権限エラーが発生する原因になります。

### 🚀 使い方

1.  GIMPで画像を開きます。
2.  メニューバーの **画像 \> フィルタ \> Pseudo Adjustment Layer** をクリックします。
3.  **【初回起動時のみ必須】** パレット下部の **`🔄 Reset List`** ボタンをクリックしてください。利用可能なGEGLフィルタを自動スキャンしてリストを構築します。
4.  リストからフィルタを選択（またはダブルクリック）すると、調整レイヤーとして適用されます。

### ⚙️ 動作環境

  * GIMP 3.0.0-RC1 以降
  * Python 3 サポートが有効な環境

### 📄 ライセンス

GPLv3
