# Ableton 操作の鉄則

実際に Live をクラッシュさせて判明したもの。守らないと作業内容が飛ぶ。

## 1. Arrangement クリップに直接ノートを書かない ❌

`add_notes_to_arrangement_clip` のような直接書き込みは **Live 12 が確実に落ちる**。
Session クリップでは同じコードが正常動作するので、Live 側が Remote Script からの
Arrangement 編集を許していないと考えられる。**2回クラッシュさせて確認済み。**

### 正しい経路

```
① get_arrangement_clip_notes            既存ノートを読み出す（読み出しは安全）
② create_clip + add_notes_to_clip       Session スロットで作り直す
③ duplicate_session_clip_to_arrangement Arrangement へ配置（既存を上書き）
```

この3ステップはすべて動作実績あり。②の時点で検証できるので、
問題があれば Arrangement に触れる前に気づける。

**③は上書きなので、実行前に必ずユーザーに `⌘S` で保存させる。**

## 2. `clip.set_notes()` を使わない ❌

Live 11 以降で非推奨。Remote Script 内では DeprecationWarning がエラー扱いになり、
**通信スレッドが死ぬ**。オリジナルの ableton-mcp はこれを使っているので Live 12 では壊れる。

```python
# ダメ
clip.set_notes(tuple(live_notes))

# 正しい（スクリプト冒頭に import Live が必要）
specs = tuple(Live.Clip.MidiNoteSpecification(
    pitch=p, start_time=st, duration=du, velocity=ve, mute=mu) for ...)
clip.add_new_notes(specs)
```

`import Live` を忘れると同じくハンドラが固まる。これも実際にやらかした。

## 3. Session ビューのスロットは既定 8 個

11 セクションのクリップを作ろうとして `Clip index out of range` で失敗した。
**同内容のセクション（Verse 1 と Verse 2 など）は 1 クリップにまとめ、
Arrangement で複数回配置する**のが正しい設計。

## 4. トラックは削除できない

~~Remote Script に削除コマンドが無い。~~ 2026-09-10 に `delete_track` を追加した（`expected_name` 必須にして誤削除を防ぐ）。それ以前は、スクリプトを二重実行してトラックが重複しても
私からは消せないので、**トラック作成は名前で存在確認してから**行う。

## 5. クラッシュしたら

1. これ以上ソケットに接続しない（悪化する）
2. `~/Library/Preferences/Ableton/Live*/Log.txt` で原因を確認
3. ユーザーに強制終了（⌥⌘Esc）を依頼
4. `.als` の最終保存時刻を確認して、どこまで戻るか伝える

## 6. 例外は握って返す

Remote Script のメソッドは必ず try/except で囲み、例外を投げ返す。
握らないとハンドラごと死んで、以後すべての通信が止まる。


## 7. 「鳴らない」と言われたら、まず測る

デバイスやプラグインを疑う前に、この順で読む。推測で触ると時間を溶かす。

```python
cmd('get_track_meters')          # mute / solo / メーター
cmd('get_track_info', {...})     # 各デバイスの Device On
cmd('get_arrangement_clip_notes', {...})   # ノートが入っているか、音域は妥当か
```

実際にあった原因（すべて測定で特定した）:

| 症状 | 原因 |
|---|---|
| 全部鳴らない | Live の出力デバイスが macOS と違う。AirPods のマイクが入力になって HFP に落ちエンジン停止 |
| ベースだけ鳴らない | MODO BASS 1.5.2 が Intel 専用（arm64 の Live では無音）。さらに**記譜音**で受けるので転写に +12 が必要 |
| MIDI が無いのに鳴る | BFD3 のプリセットがグルーヴを含み、トランスポートに同期して自動演奏していた |
| 音が小さい | メーター換算式を誤り、閉ループが全トラックを 12〜25dB 下げていた |

**音源を載せたら半音階テストクリップ（MIDI 24→60 を1拍ずつ）を空きスロットに置いて、
どの音から鳴るかを確認する。** キーマップのズレはこれで一発で分かる。

## 8. 外部プラグインの公開パラメータは載せてから数える

「外部プラグインは Device On だけ」は**思い込み**だった。

```
Heavyocity Punish  36    FabFilter Pro-L 2  17
Serum 2 / Kontakt / Saturn 2 / Pro-Q 4 / Ozone 10 / SSD5 / MODO BASS / BFD3   1
```

捨てトラックに載せて `get_device_parameters` の数を確認してから、使えるかどうかを判断する。

## 9. デバイスは削除も並べ替えもできない

順番を変えたいときは、古いものを `Device On = 0` でバイパスして末尾に追加し直す。
歪みの前にリバーブが来てしまった場合はこれで回避する。

## 10. 音量・音色の判断はメーターでなく Resampling 録音で

`get_track_meters` はピークの粗いサンプル（毎秒 2 回）で、楽器ごとのクレストファクター差があるため
ピーク基準で揃えるとドラムが埋もれる。**「小さい／大きい」の判断は Resampling 録音の RMS / LUFS で行う**
（手順は `docs/08-cover-pipeline.md` §7）。マスターのデバイスが効いているか怪しいときも、推測せず ON/OFF を録って比べる。
