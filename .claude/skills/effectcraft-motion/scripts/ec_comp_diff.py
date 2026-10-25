#!/usr/bin/env python3
"""ec-comp-diff: snapshot a comp and diff it later, to learn what Elias changed by hand.

  ec-comp-diff snap COMP [--out F]      dump the live comp (app on 9877) to F (default: snapshots dir)
  ec-comp-diff diff COMP [F]            live comp vs snapshot F (default: latest snapshot of COMP)
  ec-comp-diff dump COMP [--project P]  print a dump (live, or from a saved .ecproj via the CLI)
  ec-comp-diff list [--since ISO]       snapshots (+ project, time) for editing-retro, as JSON lines

snap also writes F.meta.json (comp id, name, project, time). diff reads the comp from that project's
saved .ecproj when the live app has another project open.

COMP = comp id or exact name. The dump lists every layer (transform, parent, matte, switches, solid
colour), every keyframe with its eases, expressions, and every mask/effect value. Read-only.
"""
import difflib, glob, json, os, socket, subprocess, sys, tempfile, time

PORT = int(os.environ.get("EFFECTCRAFT_CONTROL_PORT", "9877"))
SNAPS = os.path.expanduser("~/.cache/ec-comp-snapshots")
CLI = os.path.expanduser("~/Developer/effectcraft/target/local/local/effectcraft-cli")

JSX = r"""
var W=%s, c=null;
for(var i=1;i<=app.project.numItems;i++){var it=app.project.item(i);if(it instanceof CompItem&&(it.id==W||it.name==W))c=it;}
if(!c) throw new Error("no comp "+W);
function f(v){if(v instanceof Array){var a=[];for(var i=0;i<v.length;i++)a.push(f(v[i]));return "["+a.join(",")+"]";}
 if(typeof v=="number")return String(Math.round(v*1000)/1000); if(v&&v.vertices)return "path"+f(v.vertices); return String(v);}
var out=["comp "+c.name+" "+c.width+"x"+c.height+" "+f(c.frameRate)+"fps dur "+f(c.duration)];
function dump(p,pre,all){for(var j=1;j<=p.numProperties;j++){var q=p.property(j);if(!q)continue;
 if(q.propertyType!=PropertyType.PROPERTY){try{if(q.matchName=="ADBE Mask Atom")out.push("  "+pre+q.name+" mode "+q.maskMode+(q.inverted?" INVERTED":""));}catch(e){}dump(q,pre+q.name+"/",all||q.matchName=="ADBE Mask Parade"||q.matchName=="ADBE Effect Parade");continue;}
 try{ if(q.numKeys>0){var ks=[];for(var k=1;k<=q.numKeys;k++){var s=f(q.keyTime(k))+"s="+f(q.keyValue(k));
   try{var ie=q.keyInTemporalEase(k)[0],oe=q.keyOutTemporalEase(k)[0];s+=" in("+f(ie.speed)+","+f(ie.influence)+") out("+f(oe.speed)+","+f(oe.influence)+")";}catch(e){}ks.push(s);}
   out.push("  "+pre+q.name+": "+ks.join(" | "));}
  else if(all) out.push("  "+pre+q.name+" = "+f(q.value));
  if(q.expressionEnabled) out.push("  "+pre+q.name+" EXPR: "+q.expression);}catch(e){}}}
for(var i=1;i<=c.numLayers;i++){var L=c.layer(i),T=L.transform;
 var src="";try{if(L.source&&L.source.mainSource&&L.source.mainSource.color)src=" solid "+f(L.source.mainSource.color);else if(L.source)src=" src "+L.source.name;}catch(e){}
 out.push("## "+L.index+" "+L.name+src+" in "+f(L.inPoint)+" out "+f(L.outPoint)+(L.enabled?"":" HIDDEN")+(L.parent?" parent "+L.parent.name:"")+
  (L.hasTrackMatte?" matte "+L.trackMatteType:"")+" blend "+L.blendingMode);
 out.push("  pos "+f(T.position.value)+" scale "+f(T.scale.value)+" anchor "+f(T.anchorPoint.value)+" rot "+f(T.rotation.value)+" opac "+f(T.opacity.value));
 dump(L,"",false);}
var m=c.markerProperty;for(var k=1;k<=m.numKeys;k++)out.push("marker "+f(m.keyTime(k))+" "+m.keyValue(k).comment);
out.join("\n");
"""

def jsx(comp):
    return JSX % (comp if comp.isdigit() else json.dumps(comp))

def live(comp):
    return live_raw(jsx(comp))

def live_raw(code):
    req = {"id": 1, "method": "engine.execute",
           "params": {"command": "script.run", "params": {"code": code}, "client": "ec-comp-diff"}}
    s = socket.create_connection(("127.0.0.1", PORT), timeout=60)
    s.sendall((json.dumps(req) + "\n").encode()); buf = b""
    while not buf.endswith(b"\n"):
        d = s.recv(1 << 20)
        if not d: break
        buf += d
    r = json.loads(buf)
    if not r.get("ok"): sys.exit("app: " + str(r.get("error")))
    res = r["result"]; res = res.get("result", res) if isinstance(res, dict) else res
    if isinstance(res, dict) and res.get("error"): sys.exit("script: " + str(res["error"]))
    return res if isinstance(res, str) else json.dumps(res, indent=1)

def live_project():
    r = live_raw("var f=app.project.file; f?f.fsName:''")
    return r if isinstance(r, str) else ""

def from_project(comp, proj):
    with tempfile.NamedTemporaryFile("w", suffix=".jsx", delete=False) as t: t.write(jsx(comp))
    r = subprocess.run([CLI, proj, "script", t.name], capture_output=True, text=True)
    if r.returncode: sys.exit(r.stderr or r.stdout)
    out = r.stdout.strip()
    return json.loads(out) if out.startswith('"') else out

def latest(comp):
    fs = sorted(glob.glob(os.path.join(SNAPS, f"{comp.replace('/', '_')}--*.txt")))
    if not fs: sys.exit(f"no snapshot of {comp} in {SNAPS}")
    return fs[-1]

def main(a):
    if a[:1] == ["list"]:
        since = a[a.index("--since") + 1] if "--since" in a else ""
        for f in sorted(glob.glob(os.path.join(SNAPS, "*.txt"))):
            m = f[:-4] + ".meta.json"
            meta = json.load(open(m)) if os.path.exists(m) else {"comp": os.path.basename(f).split("--")[0]}
            meta["file"] = f
            meta.setdefault("time", time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(os.path.getmtime(f))))
            if meta["time"] >= since: print(json.dumps(meta))
        return
    if len(a) < 2 or a[0] not in ("snap", "diff", "dump"): sys.exit(__doc__)
    cmd, comp = a[0], a[1]
    if cmd == "dump":
        print(from_project(comp, a[a.index("--project") + 1]) if "--project" in a else live(comp)); return
    if cmd == "snap":
        os.makedirs(SNAPS, exist_ok=True)
        out = a[a.index("--out") + 1] if "--out" in a else os.path.join(SNAPS, f"{comp.replace('/', '_')}--{time.strftime('%Y%m%d-%H%M%S')}.txt")
        dump = live(comp)
        open(out, "w").write(dump + "\n")
        name = dump.split("\n", 1)[0].split(" ", 1)[-1].rsplit(" ", 4)[0] if dump.startswith("comp ") else comp
        json.dump({"comp": comp, "name": name, "project": live_project(),
                   "time": time.strftime("%Y-%m-%dT%H:%M:%S")}, open(out[:-4] + ".meta.json", "w"))
        print(out); return
    old = a[2] if len(a) > 2 and not a[2].startswith("--") else latest(comp)
    m = old[:-4] + ".meta.json"
    proj = a[a.index("--project") + 1] if "--project" in a else (json.load(open(m)).get("project", "") if os.path.exists(m) else "")
    new = from_project(comp, proj) if proj and proj != live_project() else live(comp)
    d = list(difflib.unified_diff(open(old).read().splitlines(), new.splitlines(), old, "live", lineterm="", n=1))
    print("\n".join(d) if d else "no changes")

if __name__ == "__main__":
    main(sys.argv[1:])
