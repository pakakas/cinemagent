import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from blender_client import send_bpy_code

def list_strips():
    code = """
import bpy
seq = bpy.context.scene.sequence_editor
if seq:
    strips = list(getattr(seq, "strips", getattr(seq, "sequences", [])))
    for s in sorted(strips, key=lambda x: (x.channel, x.frame_final_start)):
        status = "[MUTED]" if s.mute else "[ACTIVE]"
        print(f"CH {s.channel} [{s.type}] {status}: {s.name} (Visible: F{s.frame_final_start}..F{s.frame_final_end}, Dur: {s.frame_final_duration})")
else:
    print("NO_SEQUENCES")
"""
    res = send_bpy_code(code)
    return res.get("output", str(res))

if __name__ == "__main__":
    print(list_strips())
