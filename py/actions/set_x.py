import sys
import os
import json
import argparse
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from blender_client import send_bpy_code

def set_pos_x(time_val: str, px: float, channel: int = 4):
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

target_frame = parse_t("{time_val}")
seq = scene.sequence_editor
strips = [s for s in getattr(seq, "strips", getattr(seq, "sequences", [])) if s.channel == {channel} and s.type == 'MOVIE' and not s.mute]

for s in strips:
    v_start = int(s.frame_final_start)
    v_end = int(s.frame_final_end)
    if v_start <= target_frame <= v_end:
        s.transform.offset_x = {px}
        s.transform.keyframe_insert(data_path="offset_x", frame=target_frame)
        print(f"KEYFRAME_SET: {{s.name}} F{{target_frame}} = {px}px")

scene.frame_current = target_frame
if bpy.data.filepath:
    bpy.ops.wm.save_mainfile()
print(f"SET_POS_X_SUCCESS: F{{target_frame}} = {px}px")
"""
    return send_bpy_code(code)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generic Set Position X Keyframe Action")
    parser.add_argument("--time", type=str, required=True, help="Timestamp or frame")
    parser.add_argument("--px", type=float, required=True, help="Pixel offset X")
    parser.add_argument("--channel", type=int, default=4, help="Target channel")
    args = parser.parse_args()

    print(json.dumps(set_pos_x(args.time, args.px, args.channel), indent=2))
