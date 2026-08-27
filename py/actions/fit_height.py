import sys
import os
import json
import argparse
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from blender_client import send_bpy_code

def fit_height(channel: int = 4):
    code = f"""
import bpy
scene = bpy.context.scene
render_h = scene.render.resolution_y
seq = scene.sequence_editor
strips = [s for s in getattr(seq, "strips", getattr(seq, "sequences", [])) if s.channel == {channel} and s.type == 'MOVIE']

for s in strips:
    orig_h = s.elements[0].orig_height if s.elements else render_h
    scale = render_h / orig_h if orig_h > 0 else 1.0
    if hasattr(s, 'transform'):
        s.transform.scale_x = scale
        s.transform.scale_y = scale
        s.transform.origin[0] = 0.5
        s.transform.origin[1] = 0.5
        s.transform.offset_y = 0.0
if bpy.data.filepath:
    bpy.ops.wm.save_mainfile()
print(f"FIT_HEIGHT_SUCCESS: ch {channel}")
"""
    return send_bpy_code(code)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generic Fit Canvas Height Action")
    parser.add_argument("--channel", type=int, default=4, help="Target channel")
    args = parser.parse_args()

    print(json.dumps(fit_height(args.channel), indent=2))
