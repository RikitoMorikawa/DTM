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
│   ├── BFD3 Core Library/                    BFD3 Core Library (45GB, 19,329ファイル)
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

## プロジェクトの保存場所（運用ルール）

| DAW | 保存先 |
|---|---|
| **Ableton Live** | `~/Music/*Ableton/<プロジェクト名>/` — プロジェクトごとにフォルダを1つ作る |
| **Logic Pro** | `~/Music/*Logic Pro/` |

新規プロジェクトを作る／既存を移動するときは必ずこの配下に置く。
ユーザーから「Ableton のプロジェクトを作って」と言われたら、
保存先を聞き直さずに `~/Music/*Ableton/<名前>/` を既定とする。

### フォルダ名の先頭に `*` が付いている（重要）

Finder で並び順を上に固定するための命名。**シェルではグロブ文字なので必ずクォートする。**

```bash
ls "/Users/apple/Music/*Ableton/"          # ○ クォートすれば literal として通る
ls /Users/apple/Music/*Ableton/            # ✗ グロブ展開されて一致しない
find ~/Music -maxdepth 1 -name '*Ableton'  # ○ find のパターンもクォート必須
```

Python なら `os.path` にそのまま渡してよい（glob は使わない）。

## DAW

| | 用途 |
|---|---|
| **Ableton Live 12 Suite (Trial)** | Claude から操作可能。MIDI 生成・編曲の主戦場 |
| **Logic Pro** | 純正音源が優秀。ステム分割機能あり。ただし Claude からは操作不可 |

## 音源

| 種別 | 製品 |
|---|---|
| サンプラー | Kontakt 7 / 8, EastWest Opus, Reaktor 6 |
| ドラム | **SSD5 (Steven Slate Drums 5)**, **BFD3 3.5.0**（Core Library 45GB を SSD へ導入済み・2026-09-11） |
| ベース | **MODO BASS** |
| ピアノ | **Addictive Keys** |
| ギター | **Ample Guitar M (AGM3) 4.1.0** ← アコギ(Martin系)本命, Kontakt Factory Library 2（17音色）, **Session Guitarist Electric Sunburst**（パターン型） |
| ストリングス | Session Strings 2 |
| ブラス | Chris Hein Horns Pro |
| シンセ | Serum 2, Ableton 内蔵（Analog/Drift/Wavetable/Operator/Meld 等） |
| その他 Kontakt | Soul Sessions, Stacks, Lo-Fi Glow, Melted Vibes |

**Ample Guitar M (AGM3) を 2026-09-09 に導入。** アコースティックギター専用音源。
- プラグイン本体：`/Library/Audio/Plug-Ins/{VST3,Components,VST}/AGM.*`（内蔵・移動不可）
- サンプルライブラリ 7.9GB：`/Volumes/Logic_Library/Plugins/AGM_Library`（外付け・移動済み）
- 参照先の設定：`/Applications/Ample Sound/AGM/Configs/com.amplesound.AGM.inst.plist` の `InstDir`

**エレキ用のアンプシミュ（Amplitube / Neural DSP 等）は未所有。**

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

## BFD3 のインストール（2026-09-11 実施）

BFD は inMusic 傘下になり、**旧「BFD License Manager」は廃止**。後継は **inMusic Software Center**
（`/Applications/inMusic Software Center.app`、arm64 対応）。ログインは inMusic Profile。

1. Software Center → My Software → **BFD3 を ⋮ → Activate**（先に認証しないとライブラリだけ入れても起動時に止まる）
2. **BFD3 Core Library → Download** → `~/Downloads/inMusic/` に zip 48.6GB が落ちて自動展開（一時的に内蔵を 45GB 使う）
3. **Install** → ウィザードの **Data Location で必ず SSD を指定**
   `/Volumes/Logic_Library/Plugins/BFD3 Core Library`
   （既定は `~/Documents/BFD Drums/` で内蔵。ここを変えないと 45GB が内蔵に入る）
4. 書き込みは約 70MB/s、**所要 14分30秒**
5. BFD3 → ハンバーガーメニュー → **Tools → Set up content locations**
   → **REMOVE ALL** → **ADD** で SSD のパス → **RESCAN ALL**
   （インストーラは新パスを追加するだけで旧パスを消さない。337 エントリが二重に残る）
6. 検算：`~/Library/Application Support/BFD Drums/BFD3/DataPaths.xml` が
   `/Volumes/Logic_Library` だけを指していること（旧パス 0 件）
7. 動作確認後、`~/Downloads/inMusic/` の 45GB を削除

プラグイン本体（`BFD3.component` / `BFD3.vst3` v3.5.0）は arm64 ユニバーサルなので Live 12 でネイティブ動作する。

## BFD3 を Live で鳴らす（2026-09-11 実測）

- **Kits タブの `.bfd3kit` を読む。Presets タブの `.bfd3` は読まない。**
  Preset 76 個は**全部** `autoplay="true" autoplaymode="palette"` を持ち、MIDI が無くても勝手に鳴る。
  Kit 53 個は autoplay を 1 つも持たない（全数 grep で確認）。新規インスタンスは直近に開いた
  プログラムを復元するので、一度 Preset を開くと以後ずっと再現する。
- BFD3 は Live に `Device On` しか公開しない → **パレット停止も Kit 選択も GUI でしかできない**。
- 検算：MIDI が 0 発の区間で `get_track_meters` を読む。鳴っていれば autoplay。
- **Core Library 53 キットは全部アコースティック。** `90s Hip Hop` 等も中身は生キットピース＋加工。
  電子系は拡張パックを買うか、ユーザーキットピース（`.bfd3custkp`）で自前 WAV を入れる。
- キーマップは GM 準拠（Ableton 表記 C1=36 キック / D1=38 スネア / F#1=42 ハット）。
