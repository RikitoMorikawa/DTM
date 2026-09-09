# 詰まった点と解決

実際に発生した問題の記録。同じ轍を踏まないため。

## Ableton

### Live が固まる / クラッシュする
| 原因 | 対処 |
|---|---|
| `clip.set_notes()` を呼んだ | `add_new_notes` + `Live.Clip.MidiNoteSpecification` に変更。冒頭に `import Live` |
| Arrangement クリップに直接ノートを追加した | **不可能。** Session 経由に切り替える |
| Remote Script で例外を握っていない | try/except で囲んで raise し直す |

### `Clip index out of range`
Session ビューのスロットが既定 8 個しかない。セクションをユニーク化して 8 以下に収める。

### プラグインが Ableton に出てこない
環境設定 → Plug-Ins で「VST3 プラグインシステムフォルダを使用」「Audio Units を使用」をオン。
プラグインは AU/VST3 が共通の場所にあるので、Logic と Ableton で**インストールし直す必要はない**。
ただし Logic 純正音源（Studio Grand / Drum Kit Designer / Alchemy 等）は Ableton には出ない。

### プロジェクトフォルダをリネーム／移動したら AbletonMCP が消えた

環境設定 → Link・Tempo・MIDI のコントロールサーフェスの候補に `AbletonMCP` が出てこない。
ログを見ると**7スロット全部が `None`** に落ちている。

```
2026-09-09T17:23:45: info: AMidiIO: Midi Remote Scripts:
  MidiRemoteScript 1 [Control Surface="None" Input="None" Output="None"]
  ... 7スロットすべて None
```

原因は Live のユーザーライブラリのパスが旧名のまま残っていること。Remote Scripts は
この配下を見に行くので、フォルダ名を変えた時点で全部見えなくなる。

```bash
# 現在値の確認（GUI を開かずに分かる）
strings ~/Library/Preferences/Ableton/Live\ 12.4.5/Library.cfg | grep ProjectPath
#   <ProjectPath Value="/Users/apple/Music/Ableton" />   ← 存在しない旧パス
```

直し方：

1. 環境設定 → **Library** → 「Ableton ユーザーライブラリの場所」を新パスに
2. 同じ画面の「**Pack用インストールフォルダ**」も旧パスのまま残るので直す
3. **Live を再起動**（Remote Scripts の走査は起動時にしか走らない。ここを飛ばすと候補に出ない）
4. 環境設定 → Link・Tempo・MIDI → コントロールサーフェス 1 → `AbletonMCP`

ブラウザ左「場所」に登録したフォルダ（`Library.cfg` の `UserFolderInfo`）も旧パスのまま残る。

### 「メディアファイルが不明です」が自動検索で直らない

プロジェクトを移動すると、**プロジェクトフォルダの外**を参照しているサンプルが切れる。
`.als` は gzip した XML なので、何が切れているかは Live を開かずに調べられる。

```python
import gzip, re, os
x = gzip.open(als, 'rt', encoding='utf-8', errors='replace').read()
for p in set(re.findall(r'<Path Value="([^"]+)"', x)):
    if not os.path.exists(p): print('✗', p)
```

`*Ableton` のように **パスに `*` を含むフォルダは「フォルダを検索」で拾えなかった**。
確実なのは、実ファイルをプロジェクト内に置いて「プロジェクトを検索」させる方法。

```bash
mkdir -p "<Project>/Samples/Imported"
cp "<実ファイル>" "<Project>/Samples/Imported/"
# → 自動検索 → 「プロジェクトを検索」をオン → 開始
```

`.als` の `OriginalFileSize` と実ファイルのバイト数が一致していれば Live は同一と判断する。
そもそも予防するなら **ファイル → すべてを収集して保存**。

## Synthesizer V

### 歌が伴奏とズレる
**テンポが 120 のままになっていることが多い。** MIDI インポート後、必ず
Arrangement ルーラー1小節目の数値を確認する。過去に2回これでズレた。

### 書き出した WAV が Logic/Ableton とサンプルレート不一致
Render パネルの Sample Rate を **48000 Hz** に。既定は 44100。

### 歌詞が入らない
私が生成する MIDI は歌詞を **MIDI 歌詞メタイベント（FF 05）** に1音1モーラで埋め込む。
SynthV はこれを読む。読まなかった場合は分かち書きテキストを一括入力する。

### 制約
Basic 版は編集トラック3本まで／同時レンダリング2コアまで／自動調声等が使えない。
**スタンドアロンのみでプラグインとして動作しない**ため、WAV 書き出し→DAW 読み込みが必須。
Logic 内で完結したいなら Pro が必要。

## Alter/Ego（Plogue）

### 日本語に切り替えるとクラッシュ
WORDS 欄に英語のプレースホルダが残った状態で `VOICE` を `jp` にすると、
日本語形態素解析（chaSen）が落ちる。**先に日本語テキストを入れてから jp に切り替える。**

### 歌詞とメロディがズレる
Alter/Ego は MIDI の歌詞メタイベントを読まない。
WORDS 欄のテキスト行を **CC2 の値で選択**する方式。行が長いほどズレが蓄積する。
→ 日本語の歌ものでは Synthesizer V のほうが実用的。

### 歌詞を1行ずつ入力するのが面倒
`.ariap` プリセットは**プレーンな XML**。生成して読み込ませれば一括で入る。

```xml
<?xml version="1.0" ?>
<AriaPreset version="1765" productID="1017">
    <Target name="com.Plogue.Sequencer.Phoneme">
        <CustomData type="36979" size="{UTF-8バイト数}" version="0"
                    adata="1行目&#x0D;&#x0A;2行目&#x0D;&#x0A;" />
    </Target>
</AriaPreset>
```
`size` は adata の UTF-8 バイト数と一致させる。
設置先：`/Library/Application Support/Plogue/AlterEgo/Presets/com.Plogue.Sequencer.Phoneme/<カテゴリ>/`
（メニューはキャッシュされるので、その場で使うならプルダウンの `load` から直接開く）

## Kontakt / ギター音源

### 特定の音が「コンッ」と鳴ってギターらしくない
Factory Library の **Jazz Guitar** はフルアコ＋フラットワウンドのシミュレートで、
サステインが短く高域が出ないのが仕様。単音リードには不向き。
→ `Guitar Lead` / `Elektrik Guitar` / `Rock Guitar` に変更する。

### Electric Sunburst で楽譜どおりに鳴らない
**パターン演奏専用ライブラリ**。Strumming / Arpeggio / Riffs の3種しかなく、
どれも「書いた音符を鳴らす」ものではない。単音フレーズには使えない。バッキング専用。

### サビ終わりの余韻が次のセクションに被る
Electric Sunburst はコードを押さえている間パターンを鳴らし続ける。
**エンディングキー `G#1` / `A1` / `A#1`** を打って明示的に止める。
- エンディングは「その時の和音でエンディングを演奏して停止」する
- **音が出るのが仕様。ベロシティで強さを調整**できる（100 → 15 で目立たなくなる）
- 曲尾は最終和音と**同じ位置**にエンディングキーを置くと、その和音で終止する

## macOS 権限

| 症状 | 原因 |
|---|---|
| `osascript には補助アクセスは許可されません (-1728)` | ターミナルアプリ（Warp）にアクセシビリティ権限が必要。osascript や Terminal ではない |
| SynthV が外付けSSDにインストールできない | `/Library/Application Support/Dreamtonics` がローカルに存在しない。SSD 側へのシンボリックリンクを root で作成する |
| アプリバンドル内に書き込めない | 署名保護。ユーザーライブラリ側を使う |

## 自分（Claude）がやらかした失敗

| 失敗 | 原因 |
|---|---|
| ボーカルが MIDI 88 (E6) まで上がっていた | 度数計算の基準音を1オクターブ高く取った。**書いた後に音域を実測していなかった** |
| 「ピアノが全編鳴っている」と誤分析 | 各ステムを**自身の最大値で正規化**して比較した。実際はステムが −90dB の無音だった。絶対レベルを見ていなかった |
| 生成した曲が単調 | 統計値（音程分布・音符長）だけ合わせて、モチーフ・反復・展開を作曲していなかった |
| 「2度の動き」の実装で跳躍が43%に | 音階上の±2ステップ＝半音では3〜4半音。**単位を取り違えた** |
| Live を2回クラッシュさせた | 未検証の API を本番データに対していきなり実行した |

**教訓：生成物は必ず自分で測り直す。未検証の操作は退避可能な場所で先に試す。**
