
# Pseudo Adjustment Layer for GIMP 3 (v1.8)

# English
## Overview
This Python plugin utilizes GIMP 3's new Non-Destructive Editing (NDE) features to simulate a workflow similar to Photoshop's "Adjustment Layers".
When you apply a filter, it automatically generates a "Layer Group" containing the non-destructive effect and a layer mask, allowing you to readjust the values or partially apply the effect at any time.

## Release Notes (v1.8)
- Bug Fix: Fixed an issue where the dialog windows (Language selection and Reset List confirmation) were hiding behind the main GIMP window, causing the app to appear frozen.
- Bug Fix: Suppressed the massive amount of error messages in the Error Console during the "Reset List" process.
- Bug Fix: Completely rewrote the search logic so it correctly finds filters nested inside all categories, including Favorites and Custom Groups.
- Bug Fix: Added a forced UI refresh workaround. This bypasses a GIMP 3.2.2 bug where the layer dialog doesn't visually update after applying a filter until you perform an Undo/Redo.
- New Feature: Added a "Please Wait" loading screen with a spinner during the Reset List process.
- New Feature: Added support for multiple selection. You can now select multiple filters (using Ctrl or Shift) to perform bulk actions like adding to favorites, moving to groups, or hiding them.
- Improvement: Introduced a whitelist (safe list) to prevent certain safe filters (like gegl:drop-shadow and gegl:layer-styles) from being mistakenly excluded during internal tests.
- Improvement: Renamed the "Others" category to "Third-Party Filters" and allowed users to freely organize the filters inside using custom groups.

## Key Features
- Re-adjustable NDE: Even after applying, you can double-click the "fx" icon on the generated group to bring up the settings dialog and readjust the values at any time.
- Auto-generated Layer Masks: If you want to hide or reveal the effect in specific areas, simply paint with a black or white brush on the automatically generated layer mask.
- Bulk Management with Multiple Selection: Select multiple filters to quickly organize them. Right-click to move them to your favorites or custom groups, or hide unwanted ones all at once.
- Unlimited Favorite Groups: You are not limited to just one favorite list. Create as many Favorite groups as you need and rename them to suit your workflow.
- Organize Third-Party Filters: Filters classified under "Third-Party Filters" can be neatly organized into Custom Groups. You can also hide any filters you don't need.
- Translation & Renaming: Right-click any filter or category to manually rename it to whatever makes sense to you. You can also use the "Select" button at the top to automatically translate the official filters into your preferred language.

## Installation
1. Place pseudo_adjustment_layers.py into your GIMP 3 plug-ins folder.
2. (For Linux/Mac users) Make sure to give the file executable permissions.
3. Launch the plugin from the menu: Image -> Filters -> Pseudo Adjustment Layer.
4. On your first run, or after installing new GEGL filters to your PC, click the "Reset List" button at the bottom of the window to build the filter database.

## How to Use (Adjustment Layer Workflow)
1. Launch the plugin and select the filter you want to apply (e.g., Gaussian Blur).
2. A layer group will be generated automatically. To keep the layer dialog clean and simulate a single Adjustment Layer, the group is generated in a "collapsed" state by default.
3. To adjust the values, double-click the "fx" icon on the generated layer group.
4. To apply the effect partially, select the white box (Layer Mask) right next to the group and paint on the canvas with a black brush.

## Limitations & Known Issues
- Due to current GIMP 3.2.2 engine limitations, using the native "Merge Layer Group" option on a group containing NDE filters may not render the effect correctly.
- In GIMP 3.2.2, there is an internal bug where calling the official Drop Shadow (gegl:drop-shadow) via the Python API throws an error. If you want to use a drop shadow as an adjustment layer, it is highly recommended to install and use third-party alternatives, such as LinuxBeaver's drop shadows (e.g., lb:shadow).

---

# 日本語
## 概要
GIMP 3の新しい非破壊編集(NDE)機能を利用して、Photoshopの「調整レイヤー」のようなワークフローを再現するPythonプラグインです。
フィルタを適用すると、非破壊エフェクトとレイヤーマスクがセットになった「レイヤーグループ」が自動生成され、後からいつでも再調整や部分的な適用が可能になります。

## v1.8の更新内容 (Release Notes)
- バグ修正: 言語選択やReset List実行時の確認ダイアログが、GIMPのメインウィンドウの裏に隠れてフリーズしたように見える問題を修正しました。
- バグ修正: Reset List実行時にコンソールに大量のエラーメッセージが出力される問題を抑制しました。
- バグ修正: 検索機能のロジックを刷新し、すべてのカテゴリ(お気に入りやカスタムグループなど)で正しく検索がヒットするように修正しました。
- バグ修正: フィルタ適用直後にGIMPのレイヤー一覧が更新されず、Undo/Redoをするまでレイヤーグループが表示されないGIMP 3.2.2のUIバグを回避するため、画面の強制リフレッシュ処理を追加しました。
- 新機能: Reset Listの処理中に「Please Wait」の待機画面(スピナー)を表示するようにしました。
- 新機能: 複数選択に対応し、複数フィルタの一括整理(お気に入り追加、グループ移動、非表示など)が可能になりました。
- 改善: gegl:drop-shadow や gegl:layer-styles などの一部の特殊なフィルタが内部テストで誤って除外されないよう、ホワイトリスト(安全リスト)を導入しました。
- 改善: 分類できないサードパーティ製フィルタが入るカテゴリ名を「Others」から「Third-Party Filters」に変更し、内部をカスタムグループで自由に整理できるようにしました。

## 主な機能
- 再調整可能な非破壊編集: 適用後も、生成されたグループの「fx」アイコンをダブルクリックすることで、いつでも設定ダイアログを呼び出して数値を再調整できます。
- レイヤーマスクの自動生成: エフェクトを部分的に隠したい・適用したい場合は、自動生成されたレイヤーマスクを黒や白のブラシで塗るだけです。
- 複数選択による一括整理: CtrlキーやShiftキーを使った複数選択に対応しています。複数のフィルタをまとめて選択し、右クリックから一括で移動や非表示などの整理が行えます。
- 無制限のお気に入り(Favorite)グループ: お気に入りグループは1つだけではありません。用途に合わせて自由に新しいグループを複数作成し、リネームして管理できます。
- サードパーティ製フィルタの整理(Custom Group): Third-Party Filters内に分類されたフィルタ群も、右クリックから自由に「カスタムグループ」を作成して綺麗にフォルダ分けが可能です。不要なものは非表示(Hide)にして隠すこともできます。
- 翻訳・リネーム機能: フィルタ名やカテゴリ名の上で右クリックすると、手動で好きな言語や分かりやすい名前にリネームできます。また、Selectボタンを使えば各言語への自動一括翻訳も可能です。

## インストール方法
1. pseudo_adjustment_layers.py をGIMP 3のプラグインフォルダに配置します。
2. (Linux等の場合) ファイルに実行権限を付与してください。
3. メニューの Image -> Filters -> Pseudo Adjustment Layer から起動します。
4. 初回起動時や、新しくGEGLフィルタをPCにインストールした後は、プラグインウィンドウ下部の「Reset List」ボタンを押してフィルタ一覧を構築してください。

## 使い方 (調整レイヤー風のワークフロー)
1. プラグインを起動し、リストから適用したいフィルタ(例: Gaussian Blur)を選択します。
2. 自動的にレイヤーグループが生成されます。見た目をスッキリさせるため、グループはデフォルトで「折りたたまれた状態」で生成されます。
3. 数値を調整したい場合は、生成されたグループレイヤーの「fx」アイコンをダブルクリックします。
4. 部分的に適用したい場合は、グループレイヤーのすぐ右にある白い四角(レイヤーマスク)を選択し、黒いブラシで画像上を塗ってください。

## 制限事項・既知の問題
- GIMP 3.2.2の現在のエンジン制限により、非破壊フィルタが適用されたレイヤーグループに対して標準の「レイヤーグループの統合(Merge Layer Group)」を行うと、エフェクトが正常にレンダリングされない場合があります。
- GIMP 3.2.2の開発版では、公式のドロップシャドウ (gegl:drop-shadow) をPython APIから呼び出そうとするとエラーになる内部バグが存在します。ドロップシャドウを調整レイヤーとして使用したい場合は、LinuxBeaver氏などが公開しているサードパーティ製のドロップシャドウ(lb:shadowなど)をインストールして使用することを強く推奨します。