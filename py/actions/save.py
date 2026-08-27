import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from blender_client import send_bpy_code

def save_project():
    code = """
import bpy
if bpy.data.filepath:
    bpy.ops.wm.save_mainfile()
    print(f"SAVED: {bpy.data.filepath}")
else:
    print("NO_FILEPATH")
"""
    return send_bpy_code(code)

if __name__ == "__main__":
    print(json.dumps(save_project(), indent=2))
