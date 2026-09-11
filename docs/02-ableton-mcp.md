# Ableton MCP セットアップ

## 構成

```
Claude Code
    │  MCP (stdio)
    ↓
MCP_Server (Python)     /Volumes/Logic_Library/_mcp/ableton-mcp
    │  TCP socket 127.0.0.1:9877
    ↓
AbletonMCP Remote Script  ~/Music/*Ableton/User Library/Remote Scripts/AbletonMCP/   ← 実体はこちら（* 付き）。SSD 側の同名コピーは Live が読まない
    │  Live Object Model
    ↓
Ableton Live 12
```

**大量のノート投入は MCP ツールを1つずつ呼ぶより、ソケットを直接叩くほうが速い。**
`scripts/ableton_client.py` を使う。

## インストール手順

```bash
git clone https://github.com/ahujasid/ableton-mcp.git
cp -R ableton-mcp /Volumes/Logic_Library/_mcp/
cd /Volumes/Logic_Library/_mcp/ableton-mcp
uv venv .venv
uv pip install --python .venv/bin/python -e .     # ← uv venv は pip を含まないので uv pip を使う

# Remote Script を配置
mkdir -p ~/Music/Ableton/"User Library"/"Remote Scripts"/AbletonMCP
cp AbletonMCP_Remote_Script/__init__.py ~/Music/Ableton/"User Library"/"Remote Scripts"/AbletonMCP/

# Claude Code に登録
claude mcp add ableton -s user -e ABLETON_MCP_DISABLE_DATASET=1 -- \
  /Volumes/Logic_Library/_mcp/ableton-mcp/.venv/bin/python -m MCP_Server.server
```

Ableton 側：環境設定 → Link/Tempo/MIDI → Control Surface に `AbletonMCP` を選択。
画面下部に `Listening for commands on port 9877` と出れば成功。

**アプリバンドル内（/Applications/…app/Contents/）には書き込めない**（署名保護）。
必ずユーザーライブラリ側に置く。

## 適用した修正（重要）

### セキュリティ：LAN 開放を停止

オリジナルは `HOST = "0.0.0.0"` で全ネットワークインターフェースに開放される。
同じ Wi-Fi の誰でも認証なしで Ableton を操作できてしまうため `127.0.0.1` に変更。

### データ収集をオプトアウト

`MCP_Server/dataset/` に操作履歴を Supabase へ送る仕組みがある。
ソースのコメントに `Recording is ON (opt-out default)` と明記されており、
**同意を聞かれる前から記録が始まる**。
`ABLETON_MCP_DISABLE_DATASET=1` で無効化。

（作者はプライバシーに配慮しており、トラック名・クリップ名は送信前に
`<name:12>` のように伏せ字化される。ただし曲の構造と音符自体は送られる）

### Live 12 対応：set_notes → add_new_notes

`rules/ableton-rules.md` 参照。オリジナルのままでは Live 12 でノート追加が失敗する。

### 追加した自作コマンド

```python
get_arrangement_clip_notes    # Arrangement クリップのノートを読む（安全・実績あり）
add_notes_to_arrangement_clip # ❌ Live が落ちるため無効化済み
```

## 使えるコマンド一覧

```
get_session_info / get_track_info / get_script_info / get_session_snapshot
get_clip_notes / get_arrangement_clip_notes / get_device_parameters
create_midi_track / create_audio_track / set_track_name
create_clip / create_audio_clip / delete_clip / set_clip_name
add_notes_to_clip / clear_notes_from_clip
load_instrument_or_effect / set_device_parameter
duplicate_session_clip_to_arrangement / get_arrangement_clips / create_locator
start_playback / stop_playback / fire_clip / stop_clip / set_tempo
switch_to_arrangement_view / set_arrangement_time
```

### 自作で追加したコマンド

| コマンド | 用途 |
|---|---|
| `delete_track` | `expected_name` で名前照合してから削除（2026-09-10） |
| `get_track_meters` | 全トラック＋Return＋Master の `output_meter_level`。「鳴っているか」を測る唯一の手段 |
| `get_chain_device_params` / `set_chain_device_param` | Drum Rack のパッド個別（`chain_index` 指定、パラメータは名前指定） |
| `get_master_info` / `load_device_on_master` / `set_master_device_param` / `set_master_volume` | マスタートラック（2026-09-11） |

追加は **3箇所**（`SCRIPT_CAPABILITIES` / `elif command_type in [...]` のゲート / ハンドラ本体）。
ゲートを忘れると `Unknown command`。反映は Live 再起動。

### Live の保存・再起動は Claude から実行できる

アクセシビリティ権限が許可済みなので、AppleScript で操作できる。

```bash
osascript -e 'tell application "System Events" to keystroke "s" using command down'   # ⌘S
osascript -e 'tell application "Ableton Live 12 Trial" to quit'
open -a "Ableton Live 12 Trial" "<path>.als"
```

## 音源の差し替えはできる（デバイスの削除はできない）

`load_instrument_or_effect` は内部で `browser.load_item()` を呼ぶだけで、
**ブラウザでダブルクリックしたのと同じ**。Live は1トラック1インストゥルメントなので、
すでに音源が載っているトラックに読ませると**置換される**。

```
検証：捨てトラックに Analog をロード → Ample Guitar M をロード
結果：devices は ['Ample Guitar M'] の1個。Analog は消えた
```

実例（Kontakt 8 → Ample Guitar M）:

```python
cmd('load_instrument_or_effect', {'track_index': 2,
    'uri': 'query:Plugins#VST3:Ample%20Sound:Ample%20Guitar%20M'})
```

**オーディオエフェクトはチェーンの末尾に追加される（置換ではない）。**
そして**デバイス削除コマンドは無い**（`delete_clip` だけ）。誤って足したら消せないので、
未検証の URI は必ず捨てトラックで試す。ただし**トラックも削除できない**ので、
捨てトラックの後始末はユーザーに頼むことになる。

URI はブラウザから取る。推測で書くと `Browser item with URI ... not found` で落ちる。

```python
cmd('get_browser_items_at_path', {'path': 'instruments'})   # query:Synths#Analog など
cmd('get_browser_items_at_path', {'path': 'plugins/VST3'})  # メーカー名フォルダが並ぶ
```

## 外部プラグインのパラメータは見えない

| | 公開パラメータ数 |
|---|---|
| Ableton 純正（EQ Eight） | 84 |
| Ableton 純正（Operator） | 195 |
| Glue Compressor | 17 |
| **FabFilter Pro-Q 4**（AU） | **1**（`Device On` のみ） |
| **Ample Guitar M**（VST3 / AU 両方） | **1**（`Device On` のみ） |
| Addictive Keys | 16（マイクレベル・センド・Master フィルタ） |

**外部プラグインは設定値を書き込めない。** 公開するかどうかはプラグイン側の実装次第で、
Addictive Keys のようにマクロを出しているものもあるが、多くは `Device On` だけ。
つまり音色づくりを数値で詰められるのは**純正デバイスと一部のプラグインに限られる**。
それ以外は「私が設計値を出して、ユーザーが GUI で入れる」分担になる。

### 純正デバイスのパラメータは正規化値

`get_device_parameters` の `min`/`max` が `0..1` のものは実単位ではない。EQ Eight の場合：

```python
freq = 10.0 * (2200.0 ** v)          # 10Hz〜22kHz の対数。v は 0..1
Q    = 0.1  * (180.0  ** v)          # 0.1〜18 の対数
# Filter Type は列挙値 0..7
#   0:48dB LowCut 1:12dB LowCut 2:LowShelf 3:Bell 4:Notch 5:HighShelf 6:12dB HighCut 7:48dB HighCut
```

Gain は実 dB（-15..15）。Glue Compressor の Threshold も実 dB（-40..0）だが、
Attack / Release / Ratio は**選択肢のインデックス**（Ratio 0,1,2 = 2:1, 4:1, 10:1）。

**書いたあとは必ず読み戻して逆変換で検算する。** ただし列挙値は数値しか返らないので、
フィルタ種別が意図どおりかは GUI で目視してもらうしかない。

## Logic Pro との比較

| | Ableton Live | Logic Pro |
|---|---|---|
| 公式API | Live Object Model | なし |
| AppleScript | — | `open/close/save/quit` 等の汎用コマンドのみ |
| トラック/プラグインをオブジェクトとして扱えるか | ✅ | ❌ |
| Claude からの操作 | ✅ 実用的 | ❌ 事実上不可 |

Logic Pro MCP（qinnovates/logic-pro-mcp）は実在するが、
AppleScript + CGEvent + Accessibility の寄せ集めで、スター数も少ない。
アクセシビリティ権限（Mac の全操作権限）を要求する点にも注意。
