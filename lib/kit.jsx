// kit.jsx — tiny helpers on top of app.run (which calls EffectCraft engine
// commands with JSON params: the "JSON inside JSX" pattern).
var COMP = null;
function unit(comp) { return Math.min(comp.w, comp.h); }          // the comp's shorter side
function px(comp, v) { return v * unit(comp) / 1080; }            // px at 1080p → px here
function set(layer, path, value) {
  return app.run("prop.set", { layer: layer, path: path, value: value });
}
function key(layer, path, time, value) {                          // adds a keyframe
  return app.run("prop.addKey", { layer: layer, path: path, time: time, value: value });
}
function ease(layer, keys) {                                      // keys: [{path, time}]
  var sel = [];
  for (var i = 0; i < keys.length; i++) sel.push({ layer: layer, path: keys[i].path, time: keys[i].time });
  app.run("keys.select", { keys: sel });
  app.run("keys.easyEase", {});
}
function newComp(name, w, h, duration) {
  var r = app.run("comp.new", { name: name, width: w, height: h, duration: duration || 4, frameRate: 29.97 });
  COMP = { id: r.comp, name: name, w: w, h: h };                  // the current comp, for primitives that need its size
  return COMP;
}
function newShape(p) {                                            // a NEW shape layer, never added into the selected one
  app.run("layer.select", { layers: [] });
  return app.run("shape.newShape", p).layer;
}
function get(layer, path, time) {                                 // a property's value (comp seconds)
  var p = { layer: layer, path: path };
  if (time !== undefined) p.time = time;
  return app.run("prop.get", p).value;
}
function velocity(layer, path, time, v) {                         // v: {inSpeed, inInfluence, outSpeed, outInfluence}
  app.run("keys.select", { keys: [{ layer: layer, path: path, time: time }] });
  app.run("keys.velocity", v);
}
// target(name, w, h, dur) — where a scene builds. With a comp open (you're editing), the scene
// goes into it at the playhead: {isNew: false, t: playhead}. With nothing open, it makes a new
// comp: {isNew: true, t: 0}. Scenes add their background only when isNew.
function target(name, w, h, dur) {
  var active = app.project.activeItem;
  if (active && typeof SCENE_NEW_COMP === "undefined") {
    var info = app.run("comp.info", {});
    COMP = { id: info.id, name: info.name, w: info.width, h: info.height, isNew: false, t: active.time };
    return COMP;
  }
  var c = newComp(name, w, h, dur);
  c.isNew = true; c.t = 0;
  return c;
}
