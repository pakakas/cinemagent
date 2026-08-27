import bpy, json

seq_ed = getattr(bpy.context.scene, "sequence_editor", None)
seq_list = getattr(seq_ed, "sequences", None) or getattr(seq_ed, "strips", None) or []

res = []
for s in seq_list:
    if s.type == 'MOVIE':
        info = {
            "name": s.name,
            "fit_method": getattr(s, "fit_method", "N/A"),
            "use_crop": getattr(s, "use_crop", False),
            "use_translation": getattr(s, "use_translation", False)
        }
        if hasattr(s, "transform"):
            t = s.transform
            info["transform"] = {
                "scale_x": t.scale_x,
                "scale_y": t.scale_y,
                "offset_x": t.offset_x,
                "offset_y": t.offset_y,
                "rotation": t.rotation
            }
        res.append(info)

print("STRIP_TRANSFORM=" + json.dumps(res, indent=2))
