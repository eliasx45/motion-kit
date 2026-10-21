#!/usr/bin/env python3
"""Render one part of a reference comp on its own: only its layers, only during its moment.

    python3 part_preview.py references/dj3-views-counter.recipe.json --id trendArrow \\
        --layers "Arrow" --start 0 --end 1.5 [--keep "BG,Light Falloff"] [--comp "<precomp name>"]

Rebuilds the comp from its recipe in a scratch project, switches every other layer's video off
(--keep: context layers to leave on, e.g. the background; parents and adjustment layers the part
needs must be listed too), sets the work area to start..end, crops the comp to where the part
draws during that time (--full-frame: don't, for camera moves) and renders
references/parts/<id>.gif (about 480 px, 12 fps). --comp renders a precomp of the recipe instead of the main comp.
Layers are names or "#n" stack positions. EFFECTCRAFT_CLI picks the CLI.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

KIT = os.path.dirname(os.path.abspath(__file__))
CLI = os.environ.get("EFFECTCRAFT_CLI", "effectcraft-cli")


def run(*args):
    r = subprocess.run([CLI, *args], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"effectcraft-cli {' '.join(args[:3])} failed:\n{(r.stderr or r.stdout)[-2000:]}")
    return r.stdout


def names(value):
    return [n.strip() for n in (value or "").split(",") if n.strip()]


def info_size(steps_out):
    r = steps_out[-1]["result"]
    return r.get("width", 1920), r.get("height", 1080)


def part_box(proj, comp, layers, start, end, cw, ch):
    """The area the part draws in over its whole moment (union of pixel bounds at 10 times),
    with a margin, kept inside the comp. None when nothing measurable draws (nulls, off-screen)."""
    x0 = y0 = float("inf")
    x1 = y1 = float("-inf")
    for i in range(10):
        t = start + (end - start) * i / 9
        out = json.loads(run("run", proj, "comp.open", json.dumps({"comp": comp}),
                             "layer.bounds", json.dumps({"time": t, "layers": layers, "pixels": True}), "--json"))
        res = (out["result"] if isinstance(out, dict) else out)[-1]["result"]
        for l in res.get("layers", []):
            if l.get("type") == "Null" or l.get("adjustment") or not l.get("visible", True) or not l.get("opacity"):
                continue
            b = l.get("pixelBounds") or l.get("bounds")
            if not b or b[2] <= 0 or b[3] <= 0:
                continue
            x0, y0 = min(x0, b[0]), min(y0, b[1])
            x1, y1 = max(x1, b[0] + b[2]), max(y1, b[1] + b[3])
    if x0 == float("inf"):
        return None
    pad = max(0.2 * max(x1 - x0, y1 - y0), 40)
    x0, y0 = max(0, x0 - pad), max(0, y0 - pad)
    x1, y1 = min(cw, x1 + pad), min(ch, y1 + pad)
    if x1 - x0 < 16 or y1 - y0 < 16:
        return None
    return [round(x0), round(y0), round(x1 - x0), round(y1 - y0)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("recipe")
    ap.add_argument("--id", required=True)
    ap.add_argument("--layers", required=True, help="the part's layers, comma-separated")
    ap.add_argument("--keep", default="", help="context layers to leave visible")
    ap.add_argument("--start", type=float, required=True)
    ap.add_argument("--end", type=float, required=True)
    ap.add_argument("--comp", help="render this precomp of the recipe instead of the main comp")
    ap.add_argument("--full-frame", action="store_true", help="don't crop to the part (camera moves, full-frame effects)")
    a = ap.parse_args()

    recipe = os.path.abspath(a.recipe)
    with open(recipe) as f:
        comp = a.comp or json.load(f)["comp"]["name"]
    out_dir = os.path.join(KIT, "references", "parts")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, f"{a.id}.gif")

    with tempfile.TemporaryDirectory() as tmp:
        proj = os.path.join(tmp, "part.ecproj")
        run("run", "file.newProject", "{}", "comp.fromRecipe", json.dumps({"path": recipe}),
            "file.save", json.dumps({"path": proj}), "--empty")
        info = json.loads(run("run", proj, "comp.open", json.dumps({"comp": comp}), "comp.info", "{}", "--json"))
        steps_out = info["result"] if isinstance(info, dict) else info  # `run --json` without saving prints the list
        layers = steps_out[-1]["result"]["layers"]
        wanted = set(names(a.layers) + names(a.keep))
        found = {l["name"] for l in layers} | {f"#{l['index']}" for l in layers}
        missing = sorted(wanted - found)
        if missing:
            sys.exit(f"no layer {missing} in comp {comp!r}; its layers: {[l['name'] for l in layers]}")
        hide = [l["id"] for l in layers if l["name"] not in wanted and f"#{l['index']}" not in wanted]
        steps = ["comp.open", json.dumps({"comp": comp})]
        if hide:
            steps += ["layer.setSwitch", json.dumps({"layers": hide, "switch": "video", "value": False})]
        steps += ["comp.workArea", json.dumps({"start": a.start, "end": a.end}), "file.save", json.dumps({"path": proj})]
        run("run", proj, *steps)
        w, h = info_size(steps_out)
        if not a.full_frame:
            box = part_box(proj, comp, names(a.layers), a.start, a.end, w, h)
            if box:
                run("run", proj, "comp.open", json.dumps({"comp": comp}), "view.setRegionOfInterest", json.dumps({"rect": box}),
                    "comp.cropToRegionOfInterest", "{}", "file.save", json.dumps({"path": proj}))
                w, h = box[2], box[3]
        # about 480 px on the long side: full resolution for small crops, down to quarter for full frames
        res = "full" if max(w, h) <= 600 else "half" if max(w, h) <= 1100 else "third" if max(w, h) <= 1600 else "quarter"
        run("render", proj, "--comp", comp, "--out", out, "--format", "gif", "--resolution", res,
            "--fps", "12", "--work-area")
    print(os.path.relpath(out, KIT))


if __name__ == "__main__":
    main()
