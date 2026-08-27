import sys
import os
import json
import argparse
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from blender_client import send_bpy_code

def set_range_x(start_time: str, end_time: str, px: float, channel: int = 4):
    code = f"""
import bpy
scene = bpy.context.scene
fps = scene.render.fps / scene.render.fps_base if scene.render.fps_base else 25.0

def parse_t(t_val):
    s_val = str(t_val).strip()
    if ":" in s_val:
        parts = s_val.split(":")
        return int((float(parts[0]) * 60 + float(parts[1])) * fps)
    val = float(s_val)
    return int(val * fps) if val < 200.0 else int(val)

f_start = parse_t("{start_time}")
f_end = parse_t("{end_time}")

seq = scene.sequence_editor
strips = [s for s in getattr(seq, "strips", getattr(seq, "sequences", [])) if s.channel == {channel} and s.type == 'MOVIE' and not s.mute]

for s in strips:
    v_start = int(s.frame_final_start)
    v_end = int(s.frame_final_end)
    if v_start <= f_start <= v_end:
        s.transform.offset_x = {px}
        s.transform.keyframe_insert(data_path="offset_x", frame=f_start)
    if v_start <= f_end <= v_end:
        s.transform.offset_x = {px}
        s.transform.keyframe_insert(data_path="offset_x", frame=f_end)

scene.frame_current = f_start
if bpy.data.filepath:
    bpy.ops.wm.save_mainfile()
print(f"RANGE_X_SUCCESS: F{{f_start}}..F{{f_end}} = {px}px")
"""
    return send_bpy_code(code)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generic Set Range X Keyframe Action")
    parser.add_argument("--start", type=str, required=True, help="Start time/frame")
    parser.add_argument("--end", type=str, required=True, help="End time/frame")
    parser.add_argument("--px", type=float, required=True, help="Pixel offset X")
    parser.add_argument("--channel", type=int, default=4, help="Target channel")
    args = parser.parse_args()

    print(json.dumps(set_range_x(args.start, args.end, args.px, args.channel), indent=2))
