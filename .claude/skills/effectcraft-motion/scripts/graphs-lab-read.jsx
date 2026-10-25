// graphs-lab-read.jsx — reads Elias's tuned eases back from "Graphs Lab (Claude)": per pill, the
// first key's out ease and the last key's in ease, normalised to card units (speed × Δt / Δv,
// Δv = straight-line distance), in GRAPHS format. Paste the changed ones into ../assets/graphs.jsx
// and graphs.json (bezier too: x1 = out/100, y1 = x1·outSpeed, x2 = 1 − in/100, y2 = 1 − (1 − x2)·inSpeed).
var comp = null;
for (var i = 1; i <= app.project.numItems; i++) {
  var it = app.project.item(i);
  if (it.name === "Graphs Lab (Claude)") comp = it;
}
var out = {};
for (var j = 1; j <= comp.numLayers; j++) {
  var L = comp.layer(j), m = /^\d+ (.+)$/.exec(L.name);
  if (!m || / (track|label)$/.test(L.name)) continue;
  var p = L.property("ADBE Transform Group").property("ADBE Position"), k = p.numKeys;
  if (k < 2) continue;
  var a = p.keyValue(1), b = p.keyValue(k), dt = p.keyTime(k) - p.keyTime(1);
  var dv = Math.sqrt((b[0] - a[0]) * (b[0] - a[0]) + (b[1] - a[1]) * (b[1] - a[1]));
  var eo = p.keyOutTemporalEase(1)[0], ei = p.keyInTemporalEase(k)[0];
  out[m[1]] = { out: { speed: eo.speed * dt / dv, influence: eo.influence },
                "in": { speed: ei.speed * dt / dv, influence: ei.influence }, seconds: dt };
}
JSON.stringify(out, null, 1);
