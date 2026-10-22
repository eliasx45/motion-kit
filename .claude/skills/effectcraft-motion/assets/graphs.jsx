// graphs.jsx — Elias's 5 Motion Library Graphs (Devin Jatho → Graphs) as the ONLY eases.
// Card values are AE temporal ease on 2 keys, normalized: the move goes 0→1 in value over 0→1 in
// time, so a card's speed is in units of the average speed Δv/Δt. graph() scales it back:
//   real speed = card speed × Δv / Δt, per dimension (signed, so a falling value eases the same way);
//   position (spatial): one speed along the motion path, Δv = the path length (straight: the chord);
//   mask paths / shapes: progress 0→1, Δv = 1.
// out ease goes on the segment's first key, in ease on its second. Influences are the cards' %.
var GRAPHS = {
  "Fast In":                      { out: { speed: 23.75273227440283, influence: 0.5926622109416769 }, "in": { speed: 0, influence: 92.921385819053 } },
  "Fast out":                     { out: { speed: 0, influence: 100 },                                "in": { speed: 0, influence: 0.887044270833337 } },
  "Quick launch · soft landing":  { out: { speed: 0, influence: 39.878273010253906 },                 "in": { speed: 0, influence: 90.92376497056749 } },
  "Slow launch · quick finish":   { out: { speed: 0, influence: 83.00112618340385 },                  "in": { speed: 0, influence: 60.121726989746094 } },
  "Smooth emphasis":              { out: { speed: 0, influence: 70.2064355214437 },                   "in": { speed: 0, influence: 70.07315423753526 } },
  // 6th: a SAVED CURVE (Motion Library curve_presets e7e9542e30c34e4f862013ab4c2adcd5), not a Graphs-folder
  // card, not approved yet. Elias's rule: on screen → somewhere still on screen. Its influences depend on the
  // move's duration (Rule A, expoInOut below); these are the 1.0 s values.
  "Expo In-Out (Elias)":          { out: { speed: 0, influence: 65 },                                 "in": { speed: 0, influence: 66.5 } }
};
// expoInOut(d) — Rule A (Elias, 22 Oct): "65 % on both sides for a 1 second thing, the longer the sharper".
// out = clamp(65 + 30 (d − 1), 50, 90), in = min(out + 1.5, 90) (settles a touch longer than it leaves).
// His hand-shaped stage carry (80.9 / 82.5 on 1.1–1.5 s moves) sits on or above this line.
function expoInOut(d) {
  var o = Math.max(50, Math.min(90, 65 + 30 * (d - 1)));
  return { out: { speed: 0, influence: o }, "in": { speed: 0, influence: Math.min(o + 1.5, 90) } };
}
function graphCard_(name, dt) { return name === "Expo In-Out (Elias)" ? expoInOut(dt) : GRAPHS[name]; }
var GRAPH_LOG = [];                       // every graph() call, replayed by graphsFinish()
var GRAPH_TOL = 0.6 * 1001 / 30000;       // 0.6 frame (keys snap to frames): how near t0 / t1 a key must sit

function graphKeys_(layer, path) { return app.run("prop.get", { layer: layer, path: path }).keys || []; }
function graphNearest_(ks, t) {
  var best = -1, bd = GRAPH_TOL;
  for (var i = 0; i < ks.length; i++) { var d = Math.abs(ks[i].time - t); if (d <= bd) { bd = d; best = i; } }
  return best;
}
// Δv of the segment a → b, one entry per ease dimension.
function graphDelta_(path, va, vb) {
  if (typeof va === "number") return [vb - va];
  if (va && va.length !== undefined) {
    if (path === "transform/position") {                         // spatial: length along the path
      var s = 0; for (var i = 0; i < va.length; i++) s += (vb[i] - va[i]) * (vb[i] - va[i]);
      return [Math.sqrt(s)];
    }
    var d = []; for (var j = 0; j < va.length; j++) d.push(vb[j] - va[j]);
    return d;
  }
  return [1];                                                     // mask path / shape: progress 0→1
}
function graphSeg_(layer, path, ks, i, name) {
  var a = ks[i], b = ks[i + 1], dt = b.time - a.time;
  var g = graphCard_(name, dt);
  if (!g) throw new Error("graph: no card named " + name);
  var dv = graphDelta_(path, a.value, b.value);
  var so = [], si = [], io = [], ii = [];
  for (var d = 0; d < dv.length; d++) {
    so.push(g.out.speed * dv[d] / dt); si.push(g["in"].speed * dv[d] / dt);
    io.push(g.out.influence); ii.push(g["in"].influence);
  }
  app.run("keys.select", { keys: [{ layer: layer, path: path, time: a.time }] });
  app.run("keys.velocity", { outSpeed: so, outInfluence: io });
  app.run("keys.select", { keys: [{ layer: layer, path: path, time: b.time }] });
  app.run("keys.velocity", { inSpeed: si, inInfluence: ii });
}
function graphApply_(e) {
  var ks = graphKeys_(e.layer, e.path);
  var i = graphNearest_(ks, e.t0), j = graphNearest_(ks, e.t1);
  if (i < 0 || j < 0 || j <= i) throw new Error("graph: no keys at " + e.t0 + " / " + e.t1 + " on " + e.path);
  for (var k = i; k < j; k++) graphSeg_(e.layer, e.path, ks, k, e.name);   // keys added inside: each piece gets the card
}
// graph(layer, path, t0, t1, name) — put card `name` on the move t0 → t1 (comp s, keys must exist).
function graph(layer, path, t0, t1, name) {
  var e = { layer: layer, path: path, t0: t0, t1: t1, name: name };
  GRAPH_LOG.push(e);
  graphApply_(e);
}
// graphChain(layer, path, times, names) — chained keys (a pop, a punch): one card per segment.
function graphChain(layer, path, times, names) {
  for (var i = 0; i + 1 < times.length; i++) graph(layer, path, times[i], times[i + 1], names[i]);
}
// graphsFinish() — run once at the end of a scene. Keys added later (an exit starting inside a
// move) split segments and change their Δv/Δt, so every logged move is re-applied in order
// (a later move wins a segment it shares).
function graphsFinish() { for (var i = 0; i < GRAPH_LOG.length; i++) graphApply_(GRAPH_LOG[i]); }
