import sys
import os
import json
import argparse
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from blender_client import send_bpy_code, parse_time_to_frame

def seek_playhead(time_val: str):
    target_frame = parse_time_to_frame(time_val)
    code = f"""
import bpy
bpy.context.scene.frame_current = {target_frame}
print(f"SEEK_SUCCESS: Frame {target_frame}")
"""
    return send_bpy_code(code)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seek playhead to specific time/frame")
    parser.add_argument("--time", type=str, required=True, help="Time or frame to seek to (e.g. '1:04', '1585')")
    args = parser.parse_args()

    print(json.dumps(seek_playhead(args.time), indent=2))
