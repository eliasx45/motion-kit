#!/usr/bin/env python3
"""fit_graph.py — fit Elias's Graphs to a measured move (a tracked position, scale, opacity…).

Finds which Graph, start frame and end frame (and values) reproduce the samples best. With
--moves N it fits N moves that ADD UP (overlapping moves on one property: build them as stacked
nulls, one move each; see effectcraft-api.md "Overlapping moves").

  fit_graph.py SAMPLES [--moves 1] [--graphs "Quick launch · soft landing,Fast In"]
               [--fps 29.97] [--range 0:132] [--max-dur 90] [--top 3]

SAMPLES: JSON [[frame, value], …] or [{"f": frame, "v": value}, …], or CSV lines "frame,value".
Frames may be any you measured (gaps are fine). Moves may start before the first sample or end
after the last (a shot that cuts in mid-move): keys outside the comp are allowed.
numpy only.
"""
import argparse, csv, json, sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
CARDS = json.loads((HERE.parent / "assets" / "graphs.json").read_text())["graphs"]
GRAPHS = {g["name"]: (g["first_key_out"]["speed"], g["first_key_out"]["influence"] / 100,
                      g["second_key_in"]["speed"], g["second_key_in"]["influence"] / 100) for g in CARDS}
EXPO = "Expo In-Out (Elias)"


def card(name, seconds):
    if name == EXPO:  # Rule A, same as graphs.jsx expoInOut()
        o = max(50.0, min(90.0, 65 + 30 * (seconds - 1)))
        return (0.0, o / 100, 0.0, min(o + 1.5, 90.0) / 100)
    return GRAPHS[name]


_TABLES = {}


def table(name, seconds):
    """(u, progress) samples of the card's AE temporal bezier, normalised 0→1 in time and value."""
    key = (name, round(seconds, 4) if name == EXPO else None)
    if key not in _TABLES:
        so, io, si, ii = card(name, seconds)
        p = np.array([[0, 0], [io, so * io], [1 - ii, 1 - si * ii], [1, 1]], float)
        t = np.linspace(0, 1, 4001)[:, None]
        b = (1 - t) ** 3 * p[0] + 3 * (1 - t) ** 2 * t * p[1] + 3 * (1 - t) * t ** 2 * p[2] + t ** 3 * p[3]
        _TABLES[key] = (b[:, 0], b[:, 1])
    return _TABLES[key]


def progress(name, a, b, f, fps):
    ux, uy = table(name, (b - a) / fps)
    return np.interp(np.clip((f - a) / (b - a), 0, 1), ux, uy)


def peak_at(name, a, b, fps):
    ux, uy = table(name, (b - a) / fps)
    v = np.gradient(uy, ux)
    return a + (b - a) * ux[int(np.nanargmax(v))]


def load(path):
    text = Path(path).read_text().strip()
    if text[:1] in "[{":
        d = json.loads(text)
        rows = [(r["f"], r["v"]) if isinstance(r, dict) else (r[0], r[1]) for r in d]
    else:
        rows = [(float(r[0]), float(r[1])) for r in csv.reader(text.splitlines()) if r and r[0].strip()[:1] not in "#f"]
    f, v = np.array(rows, float).T
    return f, v


def best_single(F, target, others, names, a_rng, max_dur, fps, top=1, bound=np.inf):
    """Best (err, name, a, b) for one move added to the fixed `others` columns (plus an offset).

    Vectorised: project the target and every candidate curve off [1, others], then the best
    amplitude and error per candidate are closed-form."""
    Q, _ = np.linalg.qr(np.column_stack([np.ones_like(F)] + others))
    r = target - Q @ (Q.T @ target)
    rr = float(r @ r)
    a = np.array(list(a_rng), float)[:, None]
    out = []
    for name in names:
        for dur in range(3, max_dur + 1):
            ux, uy = table(name, dur / fps)
            u = np.clip((F[None, :] - a) / dur, 0, 1)
            x = np.interp(u.ravel(), ux, uy).reshape(u.shape)
            xr = x - (x @ Q) @ Q.T
            xx = np.einsum("ij,ij->i", xr, xr)
            xy = xr @ r
            err2 = rr - np.where(xx > 1e-12, xy * xy / np.maximum(xx, 1e-12), 0.0)
            e = np.sqrt(np.maximum(err2, 0) / len(F))
            # a huge move of which only a sliver is seen fits anything: not a real move
            e[np.abs(xy / np.maximum(xx, 1e-12)) > bound] = np.inf
            for i in np.argsort(e)[:top]:
                out.append((float(e[i]), name, int(a[i, 0]), int(a[i, 0]) + dur))
    out.sort(key=lambda r: r[0])
    return out[:top]


def starts(F, V, n):
    """Initial guesses: one move around each of the n biggest speed peaks in the samples."""
    order = np.argsort(F)
    f, v = F[order], V[order]
    vel = np.abs(np.gradient(v, f))
    k = np.ones(5) / 5
    vel = np.convolve(vel, k, mode="same")
    peaks = [i for i in range(len(vel)) if (i == 0 or vel[i] >= vel[i - 1]) and (i == len(vel) - 1 or vel[i] >= vel[i + 1])]
    peaks = sorted(peaks, key=lambda i: -vel[i])[:n]
    return [("Quick launch · soft landing", int(f[i]) - 10, int(f[i]) + 25) for i in sorted(peaks)]


def solve(F, V, moves, fps):
    A = np.column_stack([np.ones_like(F)] + [progress(n, a, b, F, fps) for n, a, b in moves])
    c, *_ = np.linalg.lstsq(A, V, rcond=None)
    fit = A @ c
    return c, fit, float(np.sqrt(np.mean((fit - V) ** 2))), float(np.max(np.abs(fit - V)))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("samples")
    ap.add_argument("--moves", type=int, default=1)
    ap.add_argument("--graphs", help="comma-separated Graph names to try (default: all 5 + Expo)")
    ap.add_argument("--fps", type=float, default=30000 / 1001)
    ap.add_argument("--range", help="only use samples with frame in A:B")
    ap.add_argument("--max-dur", type=int, default=90, help="longest move in frames")
    ap.add_argument("--before", type=int, default=20, help="how many frames before the first sample a move may start")
    ap.add_argument("--top", type=int, default=3, help="alternatives to list for a single move")
    args = ap.parse_args()

    F, V = load(args.samples)
    if args.range:
        lo, hi = (float(x) for x in args.range.split(":"))
        m = (F >= lo) & (F <= hi)
        F, V = F[m], V[m]
    names = [n.strip() for n in args.graphs.split(",")] if args.graphs else list(GRAPHS) + [EXPO]
    for n in names:
        if n != EXPO and n not in GRAPHS:
            sys.exit(f"no Graph named {n!r}; have: {', '.join(list(GRAPHS) + [EXPO])}")
    a_rng = range(int(F.min()) - args.before, int(F.max()))
    bound = 1.5 * (V.max() - V.min())

    def descend(moves):
        alts = None
        for _ in range(10):
            changed = False
            for k in range(len(moves)):
                others = [progress(n, a, b, F, args.fps) for j, (n, a, b) in enumerate(moves) if j != k]
                res = best_single(F, V, others, names, a_rng, args.max_dur, args.fps, top=args.top, bound=bound)
                alts = res
                if (res[0][1], res[0][2], res[0][3]) != moves[k]:
                    moves[k] = (res[0][1], res[0][2], res[0][3])
                    changed = True
            if not changed:
                break
        return moves, alts

    # Starts: greedy over all Graphs, one move per speed peak, and (several moves) greedy with
    # each single Graph; each refined by coordinate descent over all Graphs; the best wins.
    def greedy(gnames):
        out = []
        for _ in range(args.moves):
            others = [progress(n, a, b, F, args.fps) for n, a, b in out]
            _, n, a, b = best_single(F, V, others, gnames, a_rng, args.max_dur, args.fps, bound=bound)[0]
            out.append((n, a, b))
        return out

    tries = [descend(greedy(names))]
    if args.moves > 1:
        tries.append(descend(starts(F, V, args.moves)))
        tries += [descend(greedy([n])) for n in names]
    moves, alts = min(tries, key=lambda t: solve(F, V, t[0], args.fps)[2])
    moves.sort(key=lambda m: m[1])

    c, fit, rms, worst = solve(F, V, moves, args.fps)
    print(f"{len(F)} samples, frames {F.min():g}–{F.max():g}; fit RMS {rms:.2f}, worst {worst:.2f}")
    base = c[0]
    for i, ((n, a, b), d) in enumerate(zip(moves, c[1:]), 1):
        print(f"move {i}: {n}  frames {a} → {b} ({b - a} f), value {'+' if d >= 0 else ''}{d:.2f}"
              f"  (peak at f{peak_at(n, a, b, args.fps):.1f})")
    if any(a < F.min() for _, a, _ in moves):
        print("note: a move starting before the first sample is the tail of an earlier move; only its"
              " shape inside the samples is measured, its start and size are the nearest fit.")
    if len(moves) == 1:
        print(f"keys: f{moves[0][1]} = {base:.2f}, f{moves[0][2]} = {base + c[1]:.2f}")
        if alts and len(alts) > 1:
            print("next best: " + "; ".join(f"{n} {a}→{b} RMS {e:.2f}" for e, n, a, b in alts[1:]))
    else:
        print(f"start value {base:.2f}; build each move on its own stacked null (keys 0 → its value),"
              " or check whether one key chain is close enough:")
        seq = sorted(moves, key=lambda m: m[1])
        if all(seq[i][2] <= seq[i + 1][1] for i in range(len(seq) - 1)):
            print("  the moves don't overlap: one property with chained keys works.")
        else:
            print("  the moves overlap: one property can't hold them, use stacked nulls.")


if __name__ == "__main__":
    main()
