# Ableton MCP セットアップ

## 構成

```
Claude Code
    │  MCP (stdio)
    ↓
MCP_Server (Python)     /Volumes/Logic_Library/_mcp/ableton-mcp
    │  TCP socket 127.0.0.1:9877
    ↓
AbletonMCP Remote Script  ~/Music/Ableton/User Library/Remote Scripts/AbletonMCP/
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

**トラック削除コマンドは無い。**

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
