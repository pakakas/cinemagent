# @pakakas/cinemagent

Blender VSE Automation and Agentic Video Editing Engine. Part of the `pakakas` ecosystem.

## Features

- **Ripple Cut Zero Gap**: Frame-accurate cutting for video and audio with automatic gap closing.
- **Smooth Camera Pan**: Bezier curve interpolation for cinematic camera framing (Offset X and Y).
- **Auto Canvas Fit**: Automatic scaling to fit 9:16 vertical canvas (Shorts, Reels, TikTok).
- **Auto Timeline Range**: Dynamic `frame_end` adjustment based on active strip duration.
- **Modular Actions**: Single-responsibility scripts located in `py/actions/*.py`.

## Directory Structure

```text
pakakas/cinemagent/
├── package.json
├── exec.ts
└── py/
    ├── blender_client.py
    ├── vse_tools.py
    └── actions/
        ├── list.py
        ├── cut.py
        ├── set_x.py
        ├── set_range_x.py
        ├── seek.py
        ├── auto_range.py
        ├── fit_height.py
        ├── add_strip.py
        ├── mute.py
        └── save.py
```

## CLI Usage

```bash
# List timeline strips
python py/actions/list.py

# Ripple cut from 00:31 to 00:37
python py/actions/cut.py --start "0:31" --end "0:37" --channels "3,4"

# Hold Offset X at 140px from second 32 to 44
python py/actions/set_range_x.py --start "32" --end "44" --px 140 --channel 4

# Seek playhead to 1:04
python py/actions/seek.py --time "1:04"

# Auto-fit playback frame range
python py/actions/auto_range.py

# Save project
python py/actions/save.py
```
