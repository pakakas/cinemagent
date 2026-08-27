import sys
import os
import json
import argparse
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from blender_client import send_bpy_code

def add_strip(video_path: str, channel_v: int = 4, channel_a: int = 3, frame_start: int = 1):
    clean_path = video_path.replace("\\", "/")
    filename = os.path.basename(clean_path)
    code = f"""
import bpy
seq = bpy.context.scene.sequence_editor or bpy.context.scene.sequence_editor_create()
container = getattr(seq, "strips", getattr(seq, "sequences", None))

m = container.new_movie("{filename}", r"{clean_path}", channel={channel_v}, frame_start={frame_start})
s = container.new_sound("{filename}_audio", r"{clean_path}", channel={channel_a}, frame_start={frame_start})
if bpy.data.filepath:
    bpy.ops.wm.save_mainfile()
print(f"ADD_STRIP_SUCCESS: {{m.name}} (ch {channel_v}) & {{s.name}} (ch {channel_a})")
"""
    return send_bpy_code(code)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generic Add Strip Action")
    parser.add_argument("--video", type=str, required=True, help="Path to video file")
    parser.add_argument("--channel_v", type=int, default=4)
    parser.add_argument("--channel_a", type=int, default=3)
    parser.add_argument("--start", type=int, default=1)
    args = parser.parse_args()

    print(json.dumps(add_strip(args.video, args.channel_v, args.channel_a, args.start), indent=2))
