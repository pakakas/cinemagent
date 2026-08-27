import sys
import os
import json
import argparse
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from blender_client import send_bpy_code

def ripple_cut(start_time: str, end_time: str, channels: list = [3, 4]):
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

cut_start = parse_t("{start_time}")
cut_end = parse_t("{end_time}")
cut_dur = cut_end - cut_start

seq = scene.sequence_editor
container = getattr(seq, "strips", getattr(seq, "sequences", None))

if seq and container:
    all_strips = list(container)
    target_strips = [s for s in all_strips if s.channel in {channels} and not s.mute]
    
    for s in target_strips:
        v_start = int(s.frame_final_start)
        v_end = int(s.frame_final_end)
        v_dur = int(s.frame_final_duration)
        v_offset = int(s.animation_offset_start)
        
        # Case 1: Cut starts strictly inside strip and ends strictly inside strip -> Split into 2
        if v_start < cut_start and v_end > cut_end:
            left_dur = cut_start - v_start
            s.frame_final_duration = left_dur
            
            offset_r = v_offset + left_dur + cut_dur
            dur_r = v_end - cut_end
            start_r = cut_start
            
            if s.type == 'MOVIE':
                filepath = getattr(s, "filepath", "")
                r = container.new_movie(f"{{s.name}}_cut", filepath, channel=s.channel, frame_start=start_r)
                r.animation_offset_start = offset_r
                r.frame_final_duration = dur_r
                if hasattr(s, 'transform') and hasattr(r, 'transform'):
                    r.transform.scale_x = s.transform.scale_x
                    r.transform.scale_y = s.transform.scale_y
                    r.transform.origin[0] = s.transform.origin[0]
                    r.transform.origin[1] = s.transform.origin[1]
                    r.transform.offset_x = s.transform.offset_x
                    r.transform.offset_y = s.transform.offset_y
            elif s.type == 'SOUND':
                filepath = s.sound.filepath if hasattr(s, "sound") and s.sound else ""
                r = container.new_sound(f"{{s.name}}_cut", filepath, channel=s.channel, frame_start=start_r)
                r.animation_offset_start = offset_r
                r.frame_final_duration = dur_r
            print(f"CASE1_SPLIT: {{s.name}} on ch {{s.channel}}")
            
        # Case 2: Cut starts at exact beginning of strip -> Advance offset and reduce duration
        elif v_start == cut_start and v_end > cut_end:
            s.animation_offset_start = v_offset + cut_dur
            s.frame_final_duration = v_dur - cut_dur
            s.frame_start = cut_start
            print(f"CASE2_TRIM_START: {{s.name}} on ch {{s.channel}} -> new_offset={{s.animation_offset_start}}, new_dur={{s.frame_final_duration}}")
            
        # Case 3: Cut ends at exact end of strip -> Reduce duration
        elif v_start < cut_start and v_end == cut_end:
            s.frame_final_duration = cut_start - v_start
            print(f"CASE3_TRIM_END: {{s.name}} on ch {{s.channel}} -> new_dur={{s.frame_final_duration}}")
            
        # Case 4: Strip is completely inside cut range -> Remove
        elif v_start >= cut_start and v_end <= cut_end:
            container.remove(s)
            print(f"CASE4_REMOVE: {{s.name}} on ch {{s.channel}}")
            
        # Case 5: Strip is strictly after cut -> Shift left
        elif v_start >= cut_end:
            s.frame_start -= cut_dur
            print(f"CASE5_SHIFT_LEFT: {{s.name}} on ch {{s.channel}}")

    scene.frame_current = max(1, cut_start - 10)
    if bpy.data.filepath:
        bpy.ops.wm.save_mainfile()
    print(f"FIXED_CUT_SUCCESS: Cut F{{cut_start}}..F{{cut_end}} ({{cut_dur}} frames)")
"""
    return send_bpy_code(code)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generic Ripple Cut Action")
    parser.add_argument("--start", type=str, required=True, help="Start time/frame")
    parser.add_argument("--end", type=str, required=True, help="End time/frame")
    parser.add_argument("--channels", type=str, default="3,4", help="Comma-separated channels")
    args = parser.parse_args()

    chs = [int(c.strip()) for c in args.channels.split(",") if c.strip()]
    print(json.dumps(ripple_cut(args.start, args.end, chs), indent=2))
