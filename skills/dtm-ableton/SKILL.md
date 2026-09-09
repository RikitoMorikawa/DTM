---
name: dtm-ableton
description: Ableton Live を Claude から操作して作曲・編曲する。MIDI の生成、トラック作成、音源ロード、Arrangement 編集。Ableton / Live / DTM / 作曲 / 編曲 / MIDI 生成 の作業時に使う。
---

# Ableton 操作スキル

## 最初に必ず読む

- `rules/ableton-rules.md` — Live をクラッシュさせる操作の一覧
- `rules/composition-rules.md` — 作曲の設計順序と音域

## 接続確認

```bash
df -h /Volumes/Logic_Library          # SSD マウント確認
lsof -nP -iTCP:9877 -sTCP:LISTEN      # Remote Script 待ち受け確認
python3 scripts/ableton_client.py     # セッション情報とトラック一覧
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

## 報告の仕方

私は音を聴けない。**「良い音になりました」と書かない。**
測定値（音数・音域・小節数・テンポ）と設計意図だけを報告し、
音楽的な判断はユーザーに委ねる。
