// style.jsx — YOUR look, in one place. Every primitive reads from here.
// Sizes are fractions (of the comp's shorter side, or of the shape) so the
// look holds at 1920x1080, 1080x1920 and 4K alike. Times are in seconds.
var STYLE = {
  bg: {
    center: "#4d4f56",       // radial background, middle
    edge:   "#121317",       // radial background, corners
    reach:  1100 / 1920           // gradient radius, fraction of comp width
  },
  orb: {
    inner: "#9fe8ff",        // gradient centre
    mid:   "#3a7bff",        // gradient middle (stop at `midAt`)
    outer: "#1a1f6b",        // gradient edge
    midAt: 0.45,
    size:  600 / 1080,       // default diameter, fraction of the comp's shorter side
    roundness: 0.2           // rounded square corner radius, fraction of size
  },
  stroke: { color: "#ffffff", width: 0.7 },          // px at 1080p, scaled with the comp
  innerShadow: {
    color: [0.03, 0.04, 0.2, 1],
    opacity: 70,
    angle: -60,              // degrees: shadow sits bottom-right
    distance: 36 / 600,         // fraction of shape size
    size: 70 / 600,            // softness, fraction of shape size
    choke: 10
  },
  pop: {
    overshoot: 115, undershoot: 95,   // scale %, the spring
    peakAt: 0.28, dipAt: 0.42, settleAt: 0.54, fadeIn: 0.12   // seconds
  }
};
