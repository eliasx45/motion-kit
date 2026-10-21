// slideUp(layer, {at?, duration?, distance?}) — rise into place on an expo-out curve, fading in.
// The layer ends where it is now. distance is px (default from STYLE.slide).
function slideUp(layer, o) {
  o = o || {};
  var s = STYLE.slide, t0 = o.at || 0, dur = o.duration || s.duration;
  var end = get(layer, "transform/position", t0);
  var d = o.distance !== undefined ? o.distance : s.distance * unit(o.comp || COMP);
  var p = "transform/position";
  key(layer, p, t0, [end[0], end[1] + d, end[2] || 0]);
  key(layer, p, t0 + dur, end);
  velocity(layer, p, t0, { outSpeed: 0, outInfluence: s.outInfluence });
  velocity(layer, p, t0 + dur, { inSpeed: 0, inInfluence: s.inInfluence });
  key(layer, "transform/opacity", t0, 0);
  key(layer, "transform/opacity", t0 + s.fadeIn, 100);
  return layer;
}
