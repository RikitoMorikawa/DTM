# DTM プロジェクト — Claude Code 指示

## 大前提

- **私（Claude）は音を聴けない。** 音楽的な良し悪しの最終判断は必ずユーザーが行う。
  「良い音になりました」と書かない。測定値と設計意図だけを報告する。
- 重いデータ（音源・ライブラリ・仮想環境）は**外付けSSD `/Volumes/Logic_Library` に置く**。
  内蔵ドライブは本業（ITエンジニア）用に空けておく。
- SSD は常時接続ではない。作業前に `df -h /Volumes/Logic_Library` でマウント確認。

## Ableton を操作する前に必ず読む

`rules/ableton-rules.md` に、**Live をクラッシュさせる操作**が列挙してある。
特に「Arrangement クリップに直接ノートを書かない」は絶対。過去に2回 Live を落としている。

## 音域の設計

ボーカルメロディを書く前に、**歌い手（または歌声合成）の音域を確定する**。
後から変えると Logic/Ableton のプロジェクトと SynthV の両方を作り直すことになる。
- Saki AI (Lite) の実用上限は **E5〜F5 (MIDI 76-77)** 程度
- 過去に MIDI 88 (E6) まで書いてしまい全面書き直しになった事例あり

## 音名表記の注意

- **Ableton / Kontakt / NI: C3 = MIDI 60**
- **MIDI 標準・私の内部計算: C4 = MIDI 60**

1オクターブずれるので、ユーザーに音名で伝えるときは Ableton 表記に合わせる。

## 解析

音声解析は `/Volumes/Logic_Library/_analysis_venv` の Python を使う。
詳細は `docs/06-analysis.md`。
