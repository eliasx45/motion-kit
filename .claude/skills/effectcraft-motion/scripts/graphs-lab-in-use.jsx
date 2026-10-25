#include "kit.jsx"
#include "graphs.jsx"
// graphs-lab-in-use.jsx — comp "Graphs Lab – in use (Claude)": each NEW ease on its real job, with real
// Motion Library elements (Devin Jatho/Elements), at real durations. One 3 s section per ease, one
// after another in the same comp; a label at the top names the ease, a comp marker each section.
// Companion of graphs-lab.jsx (same move for every ease, for tuning). For APPROVING: does it look right
// on the thing it's for? Precomps start 2 s before their section so their own intro animation is over.
// Paste kit + graphs + this inline for the effectcraft-app MCP's run_script. New comp only; never save.
var F = 1001 / 30000, SEC = 3;
var ML = { wise: "dda82ded-9fc9-45cd-b120-a52eeb5c5d6b", heart: "708d4752-628f-41a0-bfa4-011ccd161cbf",
  phone: "2eeb6e48-5b03-4042-aabd-564571a35890", reel: "9d33f7a4-ec7b-402f-b1e1-ce7ff6174bfe",
  postcard: "7edbd74d-5e8b-494e-a655-d9e0eddd8ca9", igprofile: "d1bd0b49-35df-4125-ad14-625d79dd9966",
  yt: "c73d83e2-94ae-4b71-a459-71da34514b02", browser: "8cf46489-1882-462d-ad79-41faab0f04e0" };
var c = newComp("Graphs Lab – in use (Claude)", 1920, 1080, 7 * SEC);
var comp = null;
for (var n = 1; n <= app.project.numItems; n++) if (app.project.item(n).id === c.id) comp = app.project.item(n);
app.beginUndoGroup("Graphs Lab in use");
var bg = newShape({ kind: "rect", size: [1920, 1080], position: [960, 540], name: "BG", fill: "#0c1423", strokeWidth: 0 });
function byId(id) { for (var j = 1; j <= comp.numLayers; j++) if (comp.layer(j).id === id) return comp.layer(j); return null; }
function span(id, s) { var L = byId(id); L.inPoint = s; L.outPoint = s + SEC; return L; }
// a Motion Library element for section s: starts 2 s early so its own intro is done; returns {id, st}
function element(card, s, name) {
  var before = {}; for (var j = 1; j <= comp.numLayers; j++) before[comp.layer(j).id] = 1;
  app.run("library.insert", { id: ML[card], comp: c.id, time: 0 });
  var L = null; for (var k = 1; k <= comp.numLayers; k++) if (!before[comp.layer(k).id]) L = comp.layer(k);
  L.startTime = s - 2; L.inPoint = s; L.outPoint = s + SEC; L.name = name;
  return { id: L.id, st: s - 2 };
}
function kc(e, path, t, v) { key(e.id, path, t - e.st, v); }                       // key at comp time t
function gc(e, path, t0, t1, name) { graph(e.id, path, t0 - e.st, t1 - e.st, name); }
function set2(e, path, v) { set(e.id, path, v); }
function label(s, text) {
  var t = app.run("layer.newText", { text: text, name: "S" + (s / SEC + 1) + " label", size: 34, fill: "#c5e4ff", position: [960, 90] }).layer;
  span(t, s);
  app.run("comp.addMarker", { time: s, comment: text });
}
var s, a, b, e2, T;
// S1 Expo Out 1 (Elias): 10-10 house entrance, 100 px slide up + fade, 1 s
s = 0 * SEC; T = s + 0.7; label(s, "Expo Out 1 (Elias) · entrance, 100 px slide up · 1 s");
a = element("wise", s, "S1 Notification"); set2(a, "transform/scale", [150, 150, 100]);
kc(a, "transform/position", T, [960, 910, 0]); kc(a, "transform/position", T + 30 * F, [960, 810, 0]);
kc(a, "transform/opacity", T, 0); kc(a, "transform/opacity", T + 8 * F, 100);
gc(a, "transform/position", T, T + 30 * F, "Expo Out 1 (Elias)"); gc(a, "transform/opacity", T, T + 8 * F, "Entrance fade (Elias)");
// S2 Snap in (Devin): icon pop, scale 0 → 800 %, 12 f
s = 1 * SEC; T = s + 0.7; label(s, "Snap in (Devin) · icon pop · 12 f");
a = element("heart", s, "S2 IG heart");
try { app.run("layer.setSwitch", { layers: [a.id], "switch": "collapse", value: true }); } catch (x) {}
app.run("effect.apply", { layer: a.id, effect: "Fill" });               // the icon is black: white on navy
set2(a, "effects/#1/color", [1, 1, 1, 1]);
kc(a, "transform/scale", T, [0, 0, 100]); kc(a, "transform/scale", T + 12 * F, [800, 800, 100]);
gc(a, "transform/scale", T, T + 12 * F, "Snap in (Devin)");
// S3 Reel Pop-In (Elias): reel pops out of the phone, scale + position, 18 f
s = 2 * SEC; T = s + 0.7; label(s, "Reel Pop-In (Elias) · reel out of a phone · 18 f");
b = element("phone", s, "S3 Phone"); set2(b, "transform/scale", [30, 30, 100]); set2(b, "transform/position", [700, 540, 0]);
a = element("reel", s, "S3 Reel");
kc(a, "transform/position", T, [700, 540, 0]); kc(a, "transform/position", T + 18 * F, [1260, 540, 0]);
kc(a, "transform/scale", T, [15, 15, 100]); kc(a, "transform/scale", T + 18 * F, [42, 42, 100]);
kc(a, "transform/opacity", T, 0); kc(a, "transform/opacity", T + 3 * F, 100);
gc(a, "transform/position", T, T + 18 * F, "Reel Pop-In (Elias)"); gc(a, "transform/scale", T, T + 18 * F, "Reel Pop-In (Elias)");
// S4 Quick out, gentle land (Devin): text reveal, 60 px up + fade, 21 f
s = 3 * SEC; T = s + 0.7; label(s, "Quick out, gentle land (Devin) · text reveal · 21 f");
a = { id: app.run("layer.newText", { text: "Faceless AI pages", name: "S4 Text", size: 96, fill: "#ffffff", position: [960, 600] }).layer, st: 0 };
span(a.id, s);
kc(a, "transform/position", T, [960, 600, 0]); kc(a, "transform/position", T + 21 * F, [960, 540, 0]);
kc(a, "transform/opacity", T, 0); kc(a, "transform/opacity", T + 10 * F, 100);
gc(a, "transform/position", T, T + 21 * F, "Quick out, gentle land (Devin)"); gc(a, "transform/opacity", T, T + 10 * F, "Quick out, gentle land (Devin)");
// S5 Launch out (Devin): card leaves at full speed, down off screen, 15 f
s = 4 * SEC; T = s + 1.2; label(s, "Launch out (Devin) · exit off screen · 15 f");
a = element("postcard", s, "S5 Reel card"); set2(a, "transform/scale", [55, 55, 100]);
kc(a, "transform/position", T, [960, 540, 0]); kc(a, "transform/position", T + 15 * F, [960, 1620, 0]);
gc(a, "transform/position", T, T + 15 * F, "Launch out (Devin)");
// S6 Whip (Devin): slide transition, IG profile out left, YT channel in from right, 15 f
s = 5 * SEC; T = s + 1.0; label(s, "Whip (Devin) · slide transition · 15 f");
a = element("igprofile", s, "S6 IG profile"); set2(a, "transform/scale", [55, 55, 100]);
e2 = element("yt", s, "S6 YT channel"); set2(e2, "transform/scale", [60, 60, 100]);
kc(a, "transform/position", T, [960, 540, 0]); kc(a, "transform/position", T + 15 * F, [-700, 540, 0]);
kc(e2, "transform/position", T, [2620, 540, 0]); kc(e2, "transform/position", T + 15 * F, [960, 540, 0]);
gc(a, "transform/position", T, T + 15 * F, "Whip (Devin)"); gc(e2, "transform/position", T, T + 15 * F, "Whip (Devin)");
// S7 Expo In-Out (Elias): on → on, browser shrinks to the right side, 1 s
s = 6 * SEC; T = s + 0.8; label(s, "Expo In-Out (Elias) · on screen → on screen · 1 s");
a = element("browser", s, "S7 Browser");
kc(a, "transform/position", T, [960, 540, 0]); kc(a, "transform/position", T + 30 * F, [1380, 540, 0]);
kc(a, "transform/scale", T, [70, 70, 100]); kc(a, "transform/scale", T + 30 * F, [38, 38, 100]);
gc(a, "transform/position", T, T + 30 * F, "Expo In-Out (Elias)"); gc(a, "transform/scale", T, T + 30 * F, "Expo In-Out (Elias)");
graphsFinish();
// BG to the bottom
byId(bg).moveToEnd();
app.endUndoGroup();
c.id;
