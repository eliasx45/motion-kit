#!/usr/bin/env python3
"""check_graphs — does every moving key pair in a comp use one of Elias's Graphs?

Usage: check_graphs.py PROJECT.ecproj [--comp NAME] [--all-comps] [--md OUT.md]

A key pair "moves" when its value changes. It matches a Graph when, on every dimension that
changes, both influences are within 1 % of the card's and the normalised speeds
(speed x dt / dv) within 2 % of the card's (position: dv = straight-line length; shapes and
mask paths: dv = 1). "Expo In-Out (Elias)" is matched with the influences its duration gives
(out = clamp(65 + 30 (s - 1), 50, 90), in = min(out + 1.5, 90)). Exit status 1 when anything
is unmatched. Card values: ../assets/graphs.json (the same as the engine's keys.peakGraphs).
"""
import argparse, json, math, os, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
TICK = 254016000000
INF_TOL, SPD_TOL = 0.01, 0.02
SPATIAL = {"position"}

CARDS = [(c["name"], c["first_key_out"], c["second_key_in"])
         for c in json.load(open(os.path.join(HERE, "..", "assets", "graphs.json")))["graphs"]]


def expo(dt):
    o = max(50.0, min(90.0, 65 + 30 * (dt - 1)))
    return {"speed": 0, "influence": o}, {"speed": 0, "influence": min(o + 1.5, 90.0)}


def animated(node, trail, out):
    if isinstance(node, dict):
        if node.get("keys"):
            out.append(("/".join(trail + [node.get("match", "?")]), node))
            return
        m = node.get("match")
        for k, v in node.items():
            animated(v, trail + ([m] if (m and k == "children") else []), out)
    elif isinstance(node, list):
        for v in node:
            animated(v, trail, out)


def comps(v):
    t, x = v.get("t"), v.get("v")
    if t == "Scalar":
        return [x]
    if t in ("Vec2", "Vec3", "Color"):
        return list(x)
    return None


def fits(meas, co, ci):
    for so, io_, si, ii_ in meas:
        if abs(io_ - co["influence"]) > INF_TOL * max(co["influence"], 1) or abs(ii_ - ci["influence"]) > INF_TOL * max(ci["influence"], 1):
            return False
        if abs(so - co["speed"]) > SPD_TOL * max(1.0, abs(co["speed"])) or abs(si - ci["speed"]) > SPD_TOL * max(1.0, abs(ci["speed"])):
            return False
    return True


def check_pair(match, ka, kb):
    """→ (moves, card name or None, detail)"""
    a, b = ka["value"], kb["value"]
    ca, cb = comps(a), comps(b)
    dt = (kb["time"] - ka["time"]) / TICK
    if ca is None:
        if a == b:
            return False, None, ""
        deltas = {0: 1.0}
    elif match in SPATIAL:
        L = math.dist(ca, cb)
        if L < 1e-9:
            return False, None, ""
        deltas = {0: L}
    else:
        deltas = {d: cb[d] - ca[d] for d in range(min(len(ca), len(cb))) if abs(cb[d] - ca[d]) > 1e-9}
        if not deltas:
            return False, None, ""
    oi, ii = ka.get("out_interp", "Linear"), kb.get("in_interp", "Linear")
    if oi != "Bezier" or ii != "Bezier":
        return True, None, f"interpolation {oi}/{ii}, not Bezier"
    oe, ie = ka.get("out_ease") or [], kb.get("in_ease") or []
    meas = []
    for d, dv in deltas.items():
        eo = oe[d] if d < len(oe) else (oe[0] if oe else None)
        ei = ie[d] if d < len(ie) else (ie[0] if ie else None)
        if eo is None or ei is None:
            return True, None, f"no ease on dimension {d}"
        meas.append((eo["speed"] * dt / dv, eo["influence"] * 100, ei["speed"] * dt / dv, ei["influence"] * 100))
    for name, co, ci in CARDS:
        if fits(meas, co, ci):
            return True, name, ""
    co, ci = expo(dt)
    if fits(meas, co, ci):
        return True, "Expo In-Out (Elias)", ""
    so, io_, si, ii_ = meas[0]
    return True, None, f"out {so:.2f}x / {io_:.1f} %, in {si:.2f}x / {ii_:.1f} %"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--comp", help="comp name (default: every comp)")
    ap.add_argument("--md", help="also write a Markdown report here")
    args = ap.parse_args()
    doc = json.load(open(args.project))
    comps_ = [it for it in doc["items"].values() if it["kind"].get("type") == "Comp"
              and (not args.comp or it["name"] == args.comp)]
    if not comps_:
        sys.exit(f"no comp {args.comp!r} in {args.project}")
    total, per, bad, rows = 0, Counter(), [], []
    for c in comps_:
        fr = c["kind"].get("frame_rate") or {"num": 30000, "den": 1001}
        fps = fr["num"] / fr["den"]
        for L in c["kind"]["layers"]:
            props = []
            animated(L.get("props"), [], props)
            for path, node in props:
                ks, match = node["keys"], path.split("/")[-1]
                for i in range(len(ks) - 1):
                    moves, card, det = check_pair(match, ks[i], ks[i + 1])
                    if not moves:
                        continue
                    total += 1
                    f0, f1 = ks[i]["time"] / TICK * fps, ks[i + 1]["time"] / TICK * fps
                    row = (c["name"], L.get("name", "?"), path, f0, f1, card or "UNMATCHED", det)
                    rows.append(row)
                    if card:
                        per[card] += 1
                    else:
                        bad.append(row)
    print(f"{total - len(bad)}/{total} moving key pairs match a Graph, {len(bad)} unmatched")
    for name, n in per.most_common():
        print(f"  {n:4d}  {name}")
    for r in bad[:40]:
        print(f"  UNMATCHED {r[0]} / {r[1]} `{r[2]}` f{r[3]:.0f}->f{r[4]:.0f}: {r[6]}")
    if args.md:
        lines = [f"# Graphs check: {os.path.basename(args.project)}", "",
                 f"**{total - len(bad)} / {total} matched, {len(bad)} unmatched.**", "",
                 "| Comp | Layer | Property | Frames (layer time) | Graph | Detail |", "|---|---|---|---|---|---|"]
        lines += [f"| {r[0]} | {r[1]} | `{r[2]}` | {r[3]:.0f}→{r[4]:.0f} | {r[5]} | {r[6]} |" for r in rows]
        open(args.md, "w").write("\n".join(lines) + "\n")
        print("wrote", args.md)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
