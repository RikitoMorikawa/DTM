# Synthesizer V ワークフロー

## セットアップ済みの状態

```
アプリ   /Volumes/Logic_Library/Applications/Synthesizer V Studio Basic.app  (1.11.2)
ボイス   .../Dreamtonics/Synthesizer V Studio/databases/Saki_AI_(Lite)/
リンク   /Library/Application Support/Dreamtonics → SSD側（root権限で作成済み）
```

## ボイスの入手

- **Lite 版は AHS の配布サイトからは無くなっている。Dreamtonics のリソースサーバーにある**
  - https://resource.dreamtonics.com/download/日本語/歌声データベース/
- `.svpk` を SynthV のウィンドウにドラッグ&ドロップ
- **Synthesizer V 2 では Lite 版が非対応。** バージョン確認は Info.plist の
  `CFBundleShortVersionString`（1.x なら Lite が使える）

## 手順

1. **`*_VOCAL_for_SynthV.mid` をインポート**
   - コンダクター（テンポ）+ ボーカルの2トラック構成で書き出してある
   - 歌詞は MIDI 歌詞メタイベント（FF 05）に 1音1モーラで埋め込み済み
2. **テンポを確認**（★最重要。120 のままになっていることが多い）
3. **Voice を Saki AI (Lite) に設定**
4. **Render パネル**
   - Sample Rate **48000 Hz**
   - Bit Depth 24-bit 推奨
   - File Name を曲ごとに変える（前のファイルと混ざる）
   - Destination Folder が空欄だと書き出しに失敗する
5. `Bounce to Files`
6. DAW に **1小節目の頭**にドラッグ&ドロップ

## 書き出し後の検証

Claude 側で実測して同期を確認する。

```
期待値：全体の長さ = 小節数 × 4 × 60 ÷ BPM
        歌い出し   = (歌い出し小節 − 1) × 4 × 60 ÷ BPM
```

ズレが 0.1〜0.5 秒程度なら子音の立ち上がりぶんで正常。
数秒ズレていればテンポ不一致を疑う。

## 制約

| 項目 | Basic |
|---|---|
| 編集トラック | 3本まで |
| 同時レンダリング | 2コアまで |
| 自動調声・代替発音・ブレス分離・スクリプト | 使用不可 |
| プラグイン動作 | ❌ スタンドアロンのみ |

Logic / Ableton 内で完結したいなら **Pro が必要**。
