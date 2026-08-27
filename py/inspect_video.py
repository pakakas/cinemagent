import bpy, json

scene = bpy.context.scene
seq_ed = getattr(scene, "sequence_editor", None)
seqs = getattr(seq_ed, "sequences", None) or getattr(seq_ed, "strips", None) or []

info = {
    "file": bpy.data.filepath,
    "resolution_width": scene.render.resolution_x,
    "resolution_height": scene.render.resolution_y,
    "fps": scene.render.fps,
    "frame_start": scene.frame_start,
    "frame_end": scene.frame_end,
    "sequences": []
}

for s in seqs:
    item = {
        "name": getattr(s, "name", ""),
        "type": getattr(s, "type", ""),
        "channel": getattr(s, "channel", 0),
        "frame_start": getattr(s, "frame_start", 0),
        "frame_final_duration": getattr(s, "frame_final_duration", 0)
    }
    if hasattr(s, "filepath"):
        item["filepath"] = getattr(s, "filepath", "")
    info["sequences"].append(item)

print("INSPECT_RESULT=" + json.dumps(info, indent=2))
