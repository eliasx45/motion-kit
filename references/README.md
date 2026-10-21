# references — finished comps as recipes

Elias's important comps, converted with `comp.recipe` so agents read exactly how they're made
instead of screenshotting them. Each comp has `<slug>.recipe.json`, `<slug>.gif` and a row below.
These are references, not primitives: patterns that repeat across them become proposals
(`proposals.json`), which Elias approves before anything is built.

| Comp | Source | What it is | Length | Rebuild check | Unsupported |
|---|---|---|---|---|---|
| [DJ1 Trial Rings](dj1-trial-rings.recipe.json) ([gif](dj1-trial-rings.gif)) | Motion Library › Devin Jatho/Scenes, card `e10fa5534fad4a6bbf93cdcedcfa9d7a` | Trial Reels views ring: 693K card, dashed path, cursor clicks Post | 6.3 s @ 30 fps, 1920×1080 | PASS — PSNR/SSIM 0.945s 56.265 dB/0.99753, 3.15s 56.109 dB/0.99743, 5.355s 56.653 dB/0.99765 | none |
| [DJ2 Trial Toggle](dj2-trial-toggle.recipe.json) ([gif](dj2-trial-toggle.gif)) | Motion Library › Devin Jatho/Scenes, card `3b52e533b70b4fbb9d3ebf54a55ded17` | Trial Reels toggle with light-ray lines and reel grid, camera null rig | 5.1 s @ 30 fps, 1920×1080 | PASS — PSNR/SSIM 0.765s 56.14 dB/0.99748, 2.55s 58.423 dB/0.9986, 4.335s 58.961 dB/0.99874 | none |
