// pop(layer, {at}) — scale in with one overshoot and one small rebound, fading in.
// `at` is when it starts (comp seconds).
function pop(layer, o) {
  o = o || {};
  var p = STYLE.pop, t0 = o.at || 0;
  var keys = [[0, 0], [p.peakAt, p.overshoot], [p.dipAt, p.undershoot], [p.settleAt, 100]];
  var sel = [];
  for (var i = 0; i < keys.length; i++) {
    var t = t0 + keys[i][0], v = keys[i][1];
    key(layer, "transform/scale", t, [v, v, 100]);
    sel.push({ path: "transform/scale", time: t });
  }
  key(layer, "transform/opacity", t0, 0);
  key(layer, "transform/opacity", t0 + p.fadeIn, 100);
  sel.push({ path: "transform/opacity", time: t0 }, { path: "transform/opacity", time: t0 + p.fadeIn });
  ease(layer, sel);
  return layer;
}
