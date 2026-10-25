#include "kit.jsx"
#include "graphs.jsx"
// graphs-lab.jsx — builds comp "Graphs Lab (Claude)": every ease in graphs.jsx on one pill each,
// the same 1 s move (0.5 → 1.5 s, 1140 px), so Elias can compare and tune them side by side.
// Pill layers are named "<row> <ease name>"; graphs-lab-read.jsx reads them back after he edits.
// Copy kit.jsx (motion-kit/lib) and ../assets/graphs.jsx next to it, or paste all three inline into
// the effectcraft-app MCP's run_script (it has no #include). New comp only; never save.
var NAMES = [];
for (var n in GRAPHS) NAMES.push(n);
var T0 = 0.5, T1 = 1.5, X0 = 640, X1 = 1780;
var c = newComp("Graphs Lab (Claude)", 1920, 1080, 3);
app.beginUndoGroup("Graphs Lab");
newShape({ kind: "rect", size: [1920, 1080], position: [960, 540], name: "BG", fill: "#0c1423", strokeWidth: 0 });
for (var i = 0; i < NAMES.length; i++) {
  var y = 84 + i * 83;
  newShape({ kind: "rect", size: [X1 - X0, 2], position: [(X0 + X1) / 2, y], name: (i + 1) + " track", fill: "#236197", strokeWidth: 0 });
  app.run("layer.newText", { text: NAMES[i], name: (i + 1) + " label", size: 30, fill: "#c5e4ff", position: [330, y + 11] });
  var p = newShape({ kind: "rounded", size: [96, 40], position: [X0, y], roundness: 20, name: (i + 1) + " " + NAMES[i], fill: "#4697f3", strokeWidth: 0 });
  key(p, "transform/position", T0, [X0, y, 0]);
  key(p, "transform/position", T1, [X1, y, 0]);
  graph(p, "transform/position", T0, T1, NAMES[i]);
}
graphsFinish();
app.run("time.set", { time: 1.0 });
app.endUndoGroup();
