"""Measure how far each pill/card text's ink sits from its pill's centre (comp px), from solo renders.
usage: measure.py groups.json out.json"""
import json, socket, sys, os
import numpy as np
from PIL import Image

D = os.path.dirname(os.path.abspath(__file__))
TMP = os.path.join(D, "png"); os.makedirs(TMP, exist_ok=True)
s = socket.create_connection(("127.0.0.1", 9877), timeout=600); f = s.makefile("rw"); n = [0]

def ex(cmd, params):
    n[0] += 1
    f.write(json.dumps({"id": n[0], "method": "engine.execute", "params": {"command": cmd, "params": params, "client": "claude-pillfix"}}) + "\n"); f.flush()
    r = json.loads(f.readline())
    if "error" in r and r["error"]: raise RuntimeError(r["error"])
    return r.get("result")

def script(code):
    r = ex("script.run", {"code": code})
    return r.get("result") if isinstance(r, dict) else r

def bbox(comp, layer, t, thr):
    p = os.path.join(TMP, "x.png")
    ex("render.contactSheet", {"comp": comp, "layer": layer, "times": [t], "transparent": True, "labels": False, "cols": 1, "max_side": 1920, "path": p})
    a = np.asarray(Image.open(p).convert("RGBA"))[:, :, 3]
    ys, xs = np.nonzero(a > thr)
    if len(xs) == 0: return None
    sc = 1920.0 / a.shape[1]
    return [xs.min() * sc, ys.min() * sc, (xs.max() + 1) * sc, (ys.max() + 1) * sc]

def union(bs):
    bs = [b for b in bs if b]
    if not bs: return None
    return [min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs)]

def same(a, b, tol=1.0):
    return a and b and all(abs(x - y) <= tol for x, y in zip(a, b))

groups = json.load(open(sys.argv[1])); out = []
for g in groups:
    names = [g["shape"]] + g["texts"]
    io = json.loads(script("var c=app.project.itemByID(%d);var o=[];var N=%s;for(var i=0;i<N.length;i++){var l=c.layer(N[i]);o.push([l.inPoint,l.outPoint]);}JSON.stringify(o)" % (g["comp"], json.dumps(names))))
    a = max(x[0] for x in io); b = min(x[1] for x in io)
    if b - a < 0.3: out.append({**g, "skip": "no overlap"}); continue
    ts = [a + 0.25 + (b - a - 0.4) * k / 7.0 for k in range(8)]
    rows = []
    for t in ts:
        sb = bbox(g["comp"], g["shape"], t, 200)
        tb = union([bbox(g["comp"], tn, t, 128) for tn in g["texts"]])
        rows.append((t, sb, tb))
    best = None
    for i in range(len(rows) - 1):
        t, sb, tb = rows[i]
        if not (sb and tb): continue
        if same(sb, rows[i + 1][1]) and same(tb, rows[i + 1][2]):
            inside = tb[0] >= sb[0] and tb[2] <= sb[2] and tb[1] >= sb[1] and tb[3] <= sb[3]
            if inside and (best is None or (tb[2] - tb[0]) > (best[2][2] - best[2][0]) + 0.5):
                best = rows[i]
    if not best: out.append({**g, "skip": "no rest frame", "rows": rows}); continue
    t, sb, tb = best
    dx = (sb[0] + sb[2]) / 2 - (tb[0] + tb[2]) / 2
    dy = (sb[1] + sb[3]) / 2 - (tb[1] + tb[3]) / 2
    out.append({**g, "t": t, "shapeBox": sb, "textBox": tb, "dx": round(dx, 1), "dy": round(dy, 1)})
    print("%-32s %-28s t=%.2f dx=%+.1f dy=%+.1f" % (g["name"][:32], g["shape"][:28], t, dx, dy), flush=True)
json.dump(out, open(sys.argv[2], "w"), indent=1)
