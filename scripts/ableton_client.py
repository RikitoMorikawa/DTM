#!/usr/bin/env python3
"""Ableton Remote Script へソケット直叩きするクライアント。

MCP ツールを1つずつ呼ぶより高速。大量のノート投入に使う。
    from ableton_client import cmd, arrangement_edit
"""
import socket, json, time

HOST, PORT = "127.0.0.1", 9877


def cmd(cmd_type, params=None, timeout=30, retry=3):
    """Remote Script にコマンドを送る。接続失敗時はリトライ。"""
    last = None
    for i in range(retry):
        try:
            s = socket.create_connection((HOST, PORT), timeout=timeout)
            s.sendall(json.dumps({"type": cmd_type, "params": params or {}}).encode())
            buf = b""
            s.settimeout(timeout)
            while True:
                chunk = s.recv(65536)
                if not chunk:
                    break
                buf += chunk
                try:
                    r = json.loads(buf.decode())
                    break
                except Exception:
                    continue
            s.close()
            if r.get("status") == "error":
                raise RuntimeError("%s: %s" % (cmd_type, r.get("message")))
            res = r.get("result", r)
            return json.loads(res) if isinstance(res, str) else res
        except (ConnectionRefusedError, socket.timeout, OSError) as e:
            last = e
            time.sleep(4)
    raise last


def arrangement_edit(track_index, transform, scratch_slot=7, clip_index=0):
    """Arrangement クリップを安全に編集する。

    Arrangement への直接書き込みは Live 12 を落とすため、
    「読む → Session で作り直す → Arrangement へ戻す」経路を通る。

    transform: notes(list[dict]) を受け取り、書き戻す notes を返す関数
    ※ 上書きになるので、実行前にユーザーへ ⌘S を促すこと
    """
    v = cmd("get_arrangement_clip_notes",
            {"track_index": track_index, "clip_index": clip_index})
    notes = [{"pitch": int(n["pitch"]), "start_time": float(n["start_time"]),
              "duration": float(n["duration"]), "velocity": int(n["velocity"]),
              "mute": bool(n.get("mute", False))} for n in v["notes"]]
    out = transform(notes)

    cmd("delete_clip", {"track_index": track_index, "clip_index": scratch_slot})
    cmd("create_clip", {"track_index": track_index, "clip_index": scratch_slot,
                        "length": float(v["length"])})
    cmd("set_clip_name", {"track_index": track_index, "clip_index": scratch_slot,
                          "name": v["clip_name"]})
    for i in range(0, len(out), 120):
        cmd("add_notes_to_clip", {"track_index": track_index,
                                  "clip_index": scratch_slot, "notes": out[i:i + 120]})
    check = cmd("get_clip_notes", {"track_index": track_index, "clip_index": scratch_slot})
    if check["note_count"] != len(out):
        raise RuntimeError("書き込み数が一致しない: %d != %d" % (check["note_count"], len(out)))

    cmd("duplicate_session_clip_to_arrangement",
        {"track_index": track_index, "clip_index": scratch_slot, "destination_time": 0.0})
    time.sleep(2)
    return cmd("get_arrangement_clip_notes",
               {"track_index": track_index, "clip_index": clip_index})


# 音名変換（Ableton 表記: C3 = MIDI 60）
NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
def note_name(p):
    return "%s%d" % (NAMES[p % 12], p // 12 - 2)


if __name__ == "__main__":
    i = cmd("get_session_info")
    print("テンポ %s / トラック %s" % (i["tempo"], i["track_count"]))
    for n in range(i["track_count"]):
        t = cmd("get_track_info", {"track_index": n})
        print("  [%2d] %-20s %s" % (n, t.get("name"), [d.get("name") for d in t.get("devices", [])]))
