# 環境と所有プラグイン

## ディスク方針

**重いデータは外付けSSD `/Volumes/Logic_Library` に置く**（本業用に内蔵を空ける）。
常時接続ではないので、作業前にマウント確認すること。

```bash
df -h /Volumes/Logic_Library
```

### SSD に置いてあるもの

```
/Volumes/Logic_Library/
├── Applications/Synthesizer V Studio Basic.app
├── Library/Application Support/
│   ├── Logic/          ← /Library/... からシンボリックリンク
│   ├── GarageBand/     ← 同上
│   └── Dreamtonics/Synthesizer V Studio/databases/Saki_AI_(Lite)/
├── Plugins/
│   ├── KONTAKT/                              Kontakt ライブラリ群
│   ├── SSD5Library/                          Steven Slate Drums 5 (14GB)
│   ├── Chris Hein Horns Pro Complete (47GB)
│   ├── East West/
│   └── AlterEgo_Voices/Bones_v1002/
├── Ableton/User Library/Remote Scripts/AbletonMCP/
├── _mcp/ableton-mcp/                         Ableton MCP + venv
└── _analysis_venv/                           音声解析用 Python (numpy)
```

シンボリックリンクの作り方（root 権限が必要）:
```bash
sudo ln -s "/Volumes/Logic_Library/Library/Application Support/Dreamtonics" \
           "/Library/Application Support/Dreamtonics"
```

### 内蔵に残るもの（移動不可）

`/Library/Audio/Plug-Ins/` のプラグイン本体（約6.4GB）は OS が場所を決めているため移動できない。

## DAW

| | 用途 |
|---|---|
| **Ableton Live 12 Suite (Trial)** | Claude から操作可能。MIDI 生成・編曲の主戦場 |
| **Logic Pro** | 純正音源が優秀。ステム分割機能あり。ただし Claude からは操作不可 |

## 音源

| 種別 | 製品 |
|---|---|
| サンプラー | Kontakt 7 / 8, EastWest Opus, Reaktor 6 |
| ドラム | **SSD5 (Steven Slate Drums 5)**, BFD3（※ライブラリ未インストール・0B） |
| ベース | **MODO BASS** |
| ピアノ | **Addictive Keys** |
| ギター | Kontakt Factory Library 2（17音色）, **Session Guitarist Electric Sunburst**（パターン型） |
| ストリングス | Session Strings 2 |
| ブラス | Chris Hein Horns Pro |
| シンセ | Serum 2, Ableton 内蔵（Analog/Drift/Wavetable/Operator/Meld 等） |
| その他 Kontakt | Soul Sessions, Stacks, Lo-Fi Glow, Melted Vibes |

**ギター専用プラグイン（Ample Guitar / Amplitube / Neural DSP 等）とアンプシミュは未所有。**

## ボーカル

| | 内容 |
|---|---|
| **Synthesizer V Studio Basic** 1.11.2 | Saki AI (Lite) 導入済み。日本語歌唱の本命 |
| **Alter/Ego** (Plogue) | 無料。AU/VST で Ableton 内で動く。日本語対応だが品質は SynthV に劣る。ボイス = Bones（男声） |
| Melodyne 5 / Auto-Tune EFX | 録音済み音声の編集 |

**Basic 版はスタンドアロンのみ・3トラックまで。**
Lite 版ボイスは商用利用不可、発表時に「ライブラリ名＋ライト版を使用」の明記が必要。

## ミックス／マスタリング

FabFilter 全部入り（Pro-Q 4 / Pro-C 2 / Pro-L 2 / Pro-MB / Pro-R 2 / Pro-DS / Saturn 2 等）、
iZotope Ozone 10 / Neutron 3 Elements / Nectar 3 Elements / RX 8。

## 音名表記の違い（重要）

- **Ableton / Kontakt / NI : C3 = MIDI 60**
- **MIDI 標準 : C4 = MIDI 60**

ユーザーに伝えるときは Ableton 表記に合わせること。
