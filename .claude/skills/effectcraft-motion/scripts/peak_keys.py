#!/usr/bin/env python3
"""peak_keys.py — key frames that put each move's speed peak on its stressed syllable.

  peak_keys.py MAP.json EVENTS.json [--fps 29.97] [--md]

MAP.json: a speech map from `scripts/fork/speech-map` (words with syllables: t, vowel, stress).
EVENTS.json: [{"name": "B1 Card 0 in", "word": "content", "nth": 1, "graph": "Fast In",
               "dur": 20, "layer": "B1 Card 0", "prop": "position y", "from": 1180, "to": 600}, …]
  word   the word whose stressed syllable carries the peak (case-insensitive; "nth" picks the
         n-th time it's said, default 1); or "frame": N to give the peak frame directly
  graph  one of his Graphs or "Expo In-Out (Elias)"; dur = the move's length in frames
Peak target = the stressed syllable's vowel onset − 1 frame (taste.md, "CON-tent" = f1281).
Prints one row per event: start key, end key, peak frame and the word, as a brief's moves table
(--md) or plain text. numpy only (uses fit_graph.py next to it for the curves).
"""
import argparse, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fit_graph as fg  # noqa: E402


def stressed_vowel(words, word, nth):
    hits = [w for w in words if w["word"].strip(".,!?;:\"'").lower() == word.lower()]
    if len(hits) < nth:
        raise SystemExit(f"'{word}' is said {len(hits)} time(s), not {nth}")
    w = hits[nth - 1]
    syl = w.get("syllables") or []
    best = max(syl, key=lambda s: (s.get("stress", 0) == 1, s.get("stress", 0)), default=None)
    t = best["vowel"] if best and best.get("vowel") is not None else (best or {}).get("t", w["start"])
    return t, w


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("map")
    ap.add_argument("events")
    ap.add_argument("--fps", type=float)
    ap.add_argument("--md", action="store_true", help="print a Markdown moves table")
    a = ap.parse_args()
    m = json.loads(Path(a.map).read_text())
    fps = a.fps or m.get("fps") or 30000 / 1001
    rows = []
    for e in json.loads(Path(a.events).read_text()):
        g, dur = e["graph"], int(e["dur"])
        if "frame" in e:
            target, said = float(e["frame"]), f"f{e['frame']}"
        else:
            t, w = stressed_vowel(m["words"], e["word"], int(e.get("nth", 1)))
            target, said = t * fps - 1, f"\"{w['word']}\" (vowel f{t * fps:.1f})"
        frac = (fg.peak_at(g, 0, dur, fps)) / dur
        start = round(target - frac * dur)
        peak = fg.peak_at(g, start, start + dur, fps)
        rows.append((e.get("name", "?"), e.get("layer", ""), e.get("prop", ""), e.get("from", ""), e.get("to", ""),
                     start, start + dur, g, peak, said))
    if a.md:
        print("| Move | Layer · property | Keys (frame: value) | Graph | Speed peak (on) |")
        print("|---|---|---|---|---|")
        for n, l, p, v0, v1, s, t, g, pk, said in rows:
            print(f"| {n} | {l} · {p} | f{s}: {v0} → f{t}: {v1} | {g} | f{pk:.1f} on {said} |")
    else:
        for n, l, p, v0, v1, s, t, g, pk, said in rows:
            print(f"{n}: keys f{s} → f{t} ({g}), peak f{pk:.1f} on {said}")


if __name__ == "__main__":
    main()
