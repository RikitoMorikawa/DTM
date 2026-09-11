---
name: dtm-ableton
description: Ableton Live を Claude から操作して作曲・編曲する。MIDI の生成、トラック作成、音源ロード、Arrangement 編集。Ableton / Live / DTM / 作曲 / 編曲 / MIDI 生成 の作業時に使う。
---

# Ableton 操作スキル

## 最初に必ず読む

- `rules/ableton-rules.md` — Live をクラッシュさせる操作の一覧
- `rules/composition-rules.md` — 作曲の設計順序と音域
- `docs/08-cover-pipeline.md` — **既存曲を再現するときはこれに従う**（グリッド→楽器同定→採譜→音源→タイミング→ミックス→マスター）

## 接続確認

```bash
df -h /Volumes/Logic_Library          # SSD マウント確認
nc -z 127.0.0.1 9877 && echo MCP OK   # Remote Script 待ち受け確認
python3 scripts/ableton_client.py     # セッション情報とトラック一覧
```

**Remote Script の実体は `~/Music/*Ableton/User Library/Remote Scripts/AbletonMCP/`**（`*` 付き）。
SSD 側に同名の古いコピーがあるので、編集前に必ず両方を `grep -c add_new_notes` で比較して新しい方を特定する。

Live の保存・再起動は Claude から実行できる（アクセシビリティ権限は許可済み）。

```bash
osascript -e 'tell application "System Events" to keystroke "s" using command down'
osascript -e 'tell application "Ableton Live 12 Trial" to quit'
open -a "Ableton Live 12 Trial" "<path>.als"
```

待ち受けていない場合：Ableton の 環境設定 → Link/Tempo/MIDI → Control Surface で
`AbletonMCP` を選択。画面下部に `Listening for commands on port 9877` が出る。

## 絶対に守ること

1. **Arrangement クリップに直接ノートを書かない。** Live が落ちる。
   `scripts/ableton_client.py` の `arrangement_edit()` を使う
2. **`set_notes` を使わない。** `add_new_notes` + `Live.Clip.MidiNoteSpecification`
3. **上書き操作の前にユーザーへ `⌘S` を促す**
4. **未検証の API は空きスロットで先に試す。** 本番データにいきなり実行しない
5. **生成した MIDI は必ず音域を実測する。** 度数計算のミスで1オクターブずれた事例あり
6. **「鳴らない」と言われたらデバイスを疑う前に mute / solo とメーターを読む**
7. **音源を載せたら半音階テストクリップで実際に鳴る音域を確かめる。**
   MODO BASS は記譜音で受ける（4弦の最低音 E = MIDI 40）ので、実音の転写は +12 が必要だった

## 作業の型

```python
from scripts.ableton_client import cmd, arrangement_edit, note_name

# セクションをユニーク化して Session に置く（8スロットまで）
cmd("create_clip", {"track_index": ti, "clip_index": si, "length": bars * 4.0})
cmd("add_notes_to_clip", {"track_index": ti, "clip_index": si, "notes": notes[:120]})

# Arrangement へ曲順に配置
cmd("duplicate_session_clip_to_arrangement",
    {"track_index": ti, "clip_index": si, "destination_time": beat})
```

ノートは `{"pitch", "start_time", "duration", "velocity", "mute"}` の dict。
`start_time` と `duration` は**拍**単位（16分音符 = 0.25）。

## 自作コマンド（Remote Script に追加済み）

| コマンド | 用途 |
|---|---|
| `delete_track` | `expected_name` で名前照合してから削除 |
| `get_track_meters` | 全トラック＋Return＋Master のメーター。**「鳴っているか」を測る唯一の手段** |
| `get_chain_device_params` / `set_chain_device_param` | Drum Rack のパッド個別（`chain_index` + パラメータ名） |
| `get_master_info` / `load_device_on_master` / `set_master_device_param` / `set_master_volume` | マスタートラック |

追加するときは **3箇所**（`SCRIPT_CAPABILITIES` / `elif command_type in [...]` のゲート / ハンドラ）。
ゲートを忘れると `Unknown command`。反映は Live 再起動。

## 音量を測る・合わせる

```
dBFS = (meter - 0.9018) / 0.2102 * 20        # 0.9018 が 0dBFS
```

ゲイン調整は **EQ Eight の Output（実 dB、±12）**。トラックフェーダーに setter は無い。
パンは Utility の Balance（−1〜+1）。**鳴らない区間で音量校正をしない**（サビで無音のトラックは Verse で測る）。
Live 12 の Limiter は **`Maximize On = 1`** にしないと Ceiling が効かない。

## 音色を数値で作れるデバイス

純正（Wavetable 93 / Amp 10 / Cabinet 6 / EQ Eight 84 / Glue 17 / Tension 108）に加えて、
**Heavyocity Punish（36）** と **FabFilter Pro-L 2（17）** は外部プラグインでも全パラメータを公開している。
Serum 2 / Kontakt / Saturn 2 / Pro-Q 4 / Ozone 10 / SSD5 / MODO BASS / BFD3 は `Device On` だけ。
**外部プラグインを提案する前に捨てトラックで `get_device_parameters` の数を確認する。**

## 報告の仕方

私は音を聴けない。**「良い音になりました」と書かない。**
測定値（音数・音域・小節数・テンポ）と設計意図だけを報告し、
音楽的な判断はユーザーに委ねる。
