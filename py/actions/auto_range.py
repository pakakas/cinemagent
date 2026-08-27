import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from blender_client import send_bpy_code

def auto_fit_timeline_range():
    """Automatically set scene.frame_start and scene.frame_end to match the earliest and latest active strips."""
    code = """
import bpy
scene = bpy.context.scene
seq = scene.sequence_editor

if seq:
    strips = [s for s in getattr(seq, "strips", getattr(seq, "sequences", [])) if not s.mute]
    if strips:
        min_start = min(s.frame_final_start for s in strips)
        max_end = max(s.frame_final_end for s in strips)
        
        scene.frame_start = int(max(1, min_start))
        scene.frame_end = int(max_end)
        
        fps = scene.render.fps / scene.render.fps_base if scene.render.fps_base else 25.0
        dur_sec = (scene.frame_end - scene.frame_start) / fps
        mins = int(dur_sec // 60)
        secs = int(dur_sec % 60)
        
        print(f"AUTO_RANGE_SUCCESS: frame_start={scene.frame_start}, frame_end={scene.frame_end} (Dur: {mins}:{secs:02d})")
    else:
        print("NO_ACTIVE_STRIPS")

if bpy.data.filepath:
    bpy.ops.wm.save_mainfile()
"""
    return send_bpy_code(code)

if __name__ == "__main__":
    print(json.dumps(auto_fit_timeline_range(), indent=2))
