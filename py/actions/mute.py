import sys
import os
import json
import argparse
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from blender_client import send_bpy_code

def set_mute_channels(channels: list, mute: bool = True):
    code = f"""
import bpy
seq = bpy.context.scene.sequence_editor
if seq:
    strips = list(getattr(seq, "strips", getattr(seq, "sequences", [])))
    for s in strips:
        if s.channel in {channels}:
            s.mute = {mute}
    if bpy.data.filepath:
        bpy.ops.wm.save_mainfile()
    print(f"MUTE_SUCCESS: channels {channels} (mute={mute})")
"""
    return send_bpy_code(code)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generic Mute/Unmute Channels Action")
    parser.add_argument("--channels", type=str, default="1,2", help="Comma-separated channels")
    parser.add_argument("--unmute", action="store_true", help="Unmute instead of mute")
    args = parser.parse_args()

    chs = [int(c.strip()) for c in args.channels.split(",") if c.strip()]
    print(json.dumps(set_mute_channels(chs, mute=not args.unmute), indent=2))
