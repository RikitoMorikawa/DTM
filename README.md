# DTM 制作環境ドキュメント

Ableton Live / Logic Pro / Synthesizer V / Claude Code を組み合わせた楽曲制作の記録。

## 構成

| パス | 内容 |
|---|---|
| `CLAUDE.md` | Claude Code への常設指示 |
| `docs/` | 環境・手順・詰まった点の記録 |
| `rules/` | 作業時の鉄則（違反すると壊れる類） |
| `skills/` | Claude Code スキル |
| `scripts/` | 再利用するスクリプト |

## いま確立している経路

```
Claude Code ──socket:9877──> AbletonMCP Remote Script ──> Live Object Model ──> Ableton Live
```

Ableton は Live API を持つため、Claude から直接トラック作成・MIDI 打ち込み・音源ロードができる。
Logic Pro は AppleScript 辞書が `open/close/save/quit` 等の汎用コマンドのみで、
トラックもプラグインもオブジェクトとして存在しないため、同等のことはできない。
