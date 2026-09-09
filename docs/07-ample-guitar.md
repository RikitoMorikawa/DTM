# Ample Guitar M (AGM3)

XLN の Addictive Keys と違い、**キースイッチと発音域の制約が強い**音源。
MIDI を書く前にこの表を見ること。値はすべて同梱マニュアル
`/Applications/Ample Sound/Manuals/Main Panel Manual-AGM.pdf` から抽出した実測値。

## 音名表記

**Ample の表記は C3 = MIDI 60。Ableton / Kontakt / NI と同じ**なので、
Ableton の画面に出る音名をそのまま使ってよい（MIDI 標準の C4=60 とは1オクターブずれる）。

## キーマップ

| 略 | アーティキュレーション | キースイッチ | 発音域 |
|---|---|---|---|
| Sus | Sustain & Pop | C0 (24) | **E1–C5 (40–84)** |
| NH | Natural Harmonic | C#0 (25) | E2–C5 (52–84) |
| PM | Palm Mute | D0 (26) | E1–C5 (40–84) |
| SIO | Slide In & Slide Out | D#0 (27) | F#1–C5 (42–84) |
| LS | Legato Slide (Poly Legato) | E0 (28) | F1–C5 (41–84) |
| HP | Hammer-On & Pull-Off | F0 (29) | E1–C5 (40–84) |
| SG | Slide Guitar | F#0 (30) | F#1–C5 (42–84) |

- キースイッチ帯は **C0–F#0 (24–30)**
- 起動時のデフォルトは **Sustain**。キースイッチを1つも書かなければ Sustain で鳴る
- **F#0(30) と E1(40) の間（31–39）は死に帯**。ここに書いた音は鳴らないしキースイッチにもならない

## 発音域を外れたとき

**各弦は2半音まで下げられる**（マニュアル記載）。6弦を D に下げれば D1 (38) まで出る。
MIDI を書き換えるより、まずチューニングで解決できないか考える。

## Play Mode

| モード | 挙動 |
|---|---|
| Instrument Mode | 実楽器の制約に従う（同じ弦の2音は同時に鳴らない） |
| Keyboard Mode | 実楽器の制約なし |
| Solo Mode | 単音のみ |
| Power Chord (Fifth) Mode | 5度で鳴らす |

## パターン系プラグインとの決定的な違い

Session Guitarist（Electric Sunburst 等）は**コードを押さえるとプラグインがストロークを生成する**。
その MIDI は「低い音＝パターン切替のキースイッチ」＋「和音＝コード入力」でできている。

**この MIDI を AGM に載せ替えると、和音がそのまま鳴るだけになりストロークが消える。**
AGM 側で Strummer を組み直す別作業になる（`Manuals/Guitar Strummer.pdf`）。

判別方法：MIDI に `velocity 1〜15` や `duration 0.2` 前後の極端に短い低音が
セクションの頭・末尾に点在していたら、それはパターン切替のキースイッチ。

## インストール場所

```
プラグイン本体   /Library/Audio/Plug-Ins/{VST3,Components,VST}/AGM.*   （内蔵・移動不可）
サンプル 7.9GB   /Volumes/Logic_Library/Plugins/AGM_Library            （外付け）
参照先の設定     /Applications/Ample Sound/AGM/Configs/com.amplesound.AGM.inst.plist の InstDir
```

ライセンス状態は `com.amplesound.AGM.user.plist` の `UserID` で分かる。
`demo` ならアクティベート未完了（`/Applications/Ample Sound/ActivationManager3.app`）。

## Live のブラウザ上のパス

```
プラグイン → Ample Sound → Ample Guitar M     （VST3 / AUv2 の両方にある。VST3 推奨）
uri: query:Plugins#VST3:Ample%20Sound:Ample%20Guitar%20M
```
